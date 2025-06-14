import os
from typing import List, Dict, Any, Optional

# Firebase Admin SDK for Firestore
import firebase_admin
from firebase_admin import credentials, firestore

from google.adk.agents import Agent

# --- Service Initialization ---
db = None

def _initialize_services():
    """Initializes Firebase if not already done."""
    global db
    
    # Initialize Firebase if it hasn't been done
    if not firebase_admin._apps:
        try:
            # Construct an absolute path to the credentials file relative to this script's location
            script_dir = os.path.dirname(os.path.abspath(__file__))
            cred_path = os.path.join(script_dir, 'agent-marketplace-c93af-a8fcbc1beb09.json')

            print(f"Initializing Firebase with credentials from: {cred_path}")
            
            if not os.path.exists(cred_path):
                raise FileNotFoundError(f"Credential file not found at: {cred_path}")

            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully.")
            db = firestore.client()
        except Exception as e:
            print(f"Error initializing Firebase with direct credentials: {e}")
            raise ConnectionError(
                "Firebase initialization failed. Ensure 'agent-marketplace-c93af-a8fcbc1beb09.json' is in the same directory as this script."
            )

def get_firestore_client():
    """Get Firestore client, initializing if needed."""
    global db
    if db is None:
        _initialize_services()
    return db

def comprehensive_agent_search(
    capabilities: Optional[List[str]] = None,
    max_price: Optional[float] = None,
    min_karma: Optional[int] = None,
    sort_by: str = "karma",
    sort_order: str = "desc",
    limit: int = 10,
    agent_name_contains: Optional[str] = None,
    partial_match: bool = True
) -> List[Dict[str, Any]]:
    """
    Search for agents based on capabilities, pricing, karma, and other criteria.
    Supports both exact and partial matching for capabilities.
    
    Args:
        capabilities: List of required capabilities for exact or partial matching
        max_price: Maximum acceptable price per request in tokens
        min_karma: Minimum karma score required
        sort_by: Field to sort by ("karma", "agent_pricing", "agent_name")
        sort_order: Sort order ("asc" or "desc")
        limit: Maximum number of results to return
        agent_name_contains: Filter agents whose name contains this string
        partial_match: If True, uses partial matching for capabilities
    
    Returns:
        List of agent dictionaries matching the criteria
    """
    try:
        db = get_firestore_client()
        agents_ref = db.collection('agents')
        
        # Start building the query
        query = agents_ref
        exact_match_results = []
        
        # First, try exact matches for capabilities if specified
        if capabilities and not partial_match:
            for capability in capabilities:
                query = query.where('capabilities', 'array_contains', capability)
        
        # Apply price filter (uses single-field index)
        if max_price is not None:
            query = query.where('agent_pricing', '<=', max_price)
        
        # Apply karma filter (uses single-field index)
        if min_karma is not None:
            query = query.where('karma', '>=', min_karma)
        
        # Apply sorting (uses composite indices for multi-field queries)
        if sort_by in ['karma', 'agent_pricing', 'agent_name']:
            query = query.order_by(sort_by, direction=firestore.Query.DESCENDING if sort_order == 'desc' else firestore.Query.ASCENDING)
        
        # For partial matching or when no capabilities specified, get more results to filter client-side
        query_limit = limit * 3 if (capabilities and partial_match) else limit
        query = query.limit(query_limit)
        
        # Execute query
        results = query.stream()
        
        # Process results
        agents = []
        for doc in results:
            agent_data = doc.to_dict()
            agent_data['agent_id'] = doc.id
            
            # Apply capability partial matching if enabled
            if capabilities and partial_match:
                agent_capabilities = agent_data.get('capabilities', [])
                capability_matches = 0
                matched_capabilities = []
                
                for required_cap in capabilities:
                    # Check for exact matches first
                    if required_cap in agent_capabilities:
                        capability_matches += 2  # Higher weight for exact matches
                        matched_capabilities.append(f"{required_cap} (exact)")
                    else:
                        # Check for partial matches
                        for agent_cap in agent_capabilities:
                            if (required_cap.lower() in agent_cap.lower() or 
                                agent_cap.lower() in required_cap.lower()):
                                capability_matches += 1  # Lower weight for partial matches
                                matched_capabilities.append(f"{required_cap} → {agent_cap} (partial)")
                                break
                
                # Only include agents with at least one capability match
                if capability_matches == 0:
                    continue
                    
                # Add match score and details for ranking
                agent_data['capability_match_score'] = capability_matches
                agent_data['matched_capabilities'] = matched_capabilities
            
            # Apply name filter with partial matching
            if agent_name_contains:
                agent_name = agent_data.get('agent_name', '')
                description = agent_data.get('description', '')
                
                # Check name and description for partial matches
                if (agent_name_contains.lower() not in agent_name.lower() and 
                    agent_name_contains.lower() not in description.lower()):
                    continue
            
            agents.append(agent_data)
        
        # Sort by capability match score if partial matching was used
        if capabilities and partial_match:
            agents.sort(key=lambda x: (
                x.get('capability_match_score', 0),
                x.get('karma', 0) if sort_by == 'karma' else -x.get('agent_pricing', 0)
            ), reverse=True)
        
        # Limit final results
        agents = agents[:limit]
        
        return agents
        
    except Exception as e:
        print(f"Error searching agents: {e}")
        return []

def get_agent_by_id(agent_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a specific agent by its ID.
    
    Args:
        agent_id: The unique identifier of the agent
    
    Returns:
        Agent dictionary or None if not found
    """
    try:
        db = get_firestore_client()
        doc_ref = db.collection('agents').document(agent_id)
        doc = doc_ref.get()
        
        if doc.exists:
            agent_data = doc.to_dict()
            agent_data['agent_id'] = doc.id
            return agent_data
        else:
            return None
            
    except Exception as e:
        print(f"Error retrieving agent {agent_id}: {e}")
        return None

def get_top_agents_by_capability(
    capability: str,
    limit: int = 5,
    sort_by: str = "karma",
    partial_match: bool = True
) -> List[Dict[str, Any]]:
    """
    Get the top agents with a specific capability.
    Supports both exact and partial matching for capabilities.
    
    Args:
        capability: The specific capability to search for
        limit: Number of top agents to return
        sort_by: Sort criteria ("karma" or "agent_pricing")
        partial_match: If True, includes partial matches for capabilities
    
    Returns:
        List of top agents with the specified capability
    """
    try:
        db = get_firestore_client()
        agents_ref = db.collection('agents')
        
        if not partial_match:
            # Use exact matching with composite indices
            if sort_by == "karma":
                query = agents_ref.where('capabilities', 'array_contains', capability).order_by('karma', direction=firestore.Query.DESCENDING).limit(limit)
            elif sort_by == "agent_pricing":
                query = agents_ref.where('capabilities', 'array_contains', capability).order_by('agent_pricing', direction=firestore.Query.ASCENDING).limit(limit)
            else:
                query = agents_ref.where('capabilities', 'array_contains', capability).limit(limit)
        else:
            # For partial matching, get more results and filter client-side
            query_limit = limit * 5  # Get more results for better partial matching
            if sort_by == "karma":
                query = agents_ref.order_by('karma', direction=firestore.Query.DESCENDING).limit(query_limit)
            elif sort_by == "agent_pricing":
                query = agents_ref.order_by('agent_pricing', direction=firestore.Query.ASCENDING).limit(query_limit)
            else:
                query = agents_ref.limit(query_limit)
        
        results = query.stream()
        
        agents = []
        for doc in results:
            agent_data = doc.to_dict()
            agent_data['agent_id'] = doc.id
            
            if partial_match:
                # Check for partial capability matches
                agent_capabilities = agent_data.get('capabilities', [])
                match_found = False
                match_score = 0
                matched_capability = None
                
                # Check for exact match first
                if capability in agent_capabilities:
                    match_found = True
                    match_score = 2
                    matched_capability = f"{capability} (exact)"
                else:
                    # Check for partial matches
                    for agent_cap in agent_capabilities:
                        if (capability.lower() in agent_cap.lower() or 
                            agent_cap.lower() in capability.lower()):
                            match_found = True
                            match_score = 1
                            matched_capability = f"{capability} → {agent_cap} (partial)"
                            break
                
                if not match_found:
                    continue
                    
                agent_data['capability_match_score'] = match_score
                agent_data['matched_capability'] = matched_capability
            
            agents.append(agent_data)
        
        # Sort by match score if partial matching was used
        if partial_match:
            agents.sort(key=lambda x: (
                x.get('capability_match_score', 0),
                x.get('karma', 0) if sort_by == 'karma' else -x.get('agent_pricing', 0)
            ), reverse=True)
        
        # Limit final results
        agents = agents[:limit]
        
        return agents
        
    except Exception as e:
        print(f"Error getting top agents for capability {capability}: {e}")
        return []

def get_best_value_agents(
    capability: Optional[str] = None,
    limit: int = 10,
    partial_match: bool = True
) -> List[Dict[str, Any]]:
    """
    Get agents with the best value (high karma, low price).
    Supports both exact and partial matching for capabilities.
    
    Args:
        capability: Optional capability filter
        limit: Number of agents to return
        partial_match: If True, includes partial matches for capabilities
    
    Returns:
        List of best value agents
    """
    try:
        db = get_firestore_client()
        agents_ref = db.collection('agents')
        
        if capability and not partial_match:
            # Use exact matching with composite index
            query = agents_ref.where('capabilities', 'array_contains', capability)
        else:
            # For partial matching or no capability filter, get more results
            query = agents_ref
        
        # Sort by karma (desc) then by pricing (asc) for best value
        query_limit = limit * 3 if (capability and partial_match) else limit
        query = query.order_by('karma', direction=firestore.Query.DESCENDING).order_by('agent_pricing', direction=firestore.Query.ASCENDING).limit(query_limit)
        
        results = query.stream()
        
        agents = []
        for doc in results:
            agent_data = doc.to_dict()
            agent_data['agent_id'] = doc.id
            
            # Apply capability filtering with partial matching if enabled
            if capability and partial_match:
                agent_capabilities = agent_data.get('capabilities', [])
                match_found = False
                match_score = 0
                matched_capability = None
                
                # Check for exact match first
                if capability in agent_capabilities:
                    match_found = True
                    match_score = 2
                    matched_capability = f"{capability} (exact)"
                else:
                    # Check for partial matches
                    for agent_cap in agent_capabilities:
                        if (capability.lower() in agent_cap.lower() or 
                            agent_cap.lower() in capability.lower()):
                            match_found = True
                            match_score = 1
                            matched_capability = f"{capability} → {agent_cap} (partial)"
                            break
                
                if not match_found:
                    continue
                    
                agent_data['capability_match_score'] = match_score
                agent_data['matched_capability'] = matched_capability
            
            # Calculate value score (karma per token)
            agent_data['value_score'] = agent_data.get('karma', 0) / max(agent_data.get('agent_pricing', 0.01), 0.01)
            agents.append(agent_data)
        
        # Sort by capability match score and value if partial matching was used
        if capability and partial_match:
            agents.sort(key=lambda x: (
                x.get('capability_match_score', 0),
                x.get('value_score', 0)
            ), reverse=True)
        
        # Limit final results
        agents = agents[:limit]
        
        return agents
        
    except Exception as e:
        print(f"Error getting best value agents: {e}")
        return []

agent_finder = Agent(
    model='gemini-2.0-flash-001',
    name='agent_finder',
    description='A agent that can retrieve information about available agents capable of fulfilling a given task.',
    instruction="""You are the Discovery Agent for an AI agent marketplace. Your core function is to find and rank optimal agents for specific tasks using attribute-based search with both exact and partial matching capabilities.

                    ## Available Tools:
                    - comprehensive_agent_search: Main search with filters for capabilities, pricing, karma, and sorting. Supports partial matching for capabilities and descriptions.
                    - get_agent_by_id: Get specific agent details by ID
                    - get_top_agents_by_capability: Top-rated agents for specific skills. Supports partial capability matching.
                    - get_best_value_agents: Best karma-to-price ratio agents. Supports partial capability matching.

                    ## Search Protocol:
                    1. **Analyze task complexity** - Determine if single or multi-agent approach needed
                    2. **Smart matching strategy** - Use partial matching by default for better results:
                       - Partial matching finds agents with related/similar capabilities
                       - Exact matches get higher ranking scores
                       - Searches capabilities, names, and descriptions for partial matches
                    3. **Progressive broadening** - If still no matches found, broaden further:
                       - Relax price limits (+50-100%)  
                       - Lower karma thresholds (-25-50%)
                       - Try broader capability categories
                       - Fallback: get_best_value_agents() without capability filters
                    4. **Explain results** - When presenting results, explain match types (exact vs partial)

                    ## Partial Matching Benefits:
                    - **"data_analysis"** matches agents with "data_science", "statistical_analysis", "analytics"
                    - **"web_development"** matches "frontend_development", "backend_development", "web_design"
                    - **"content_creation"** matches "copywriting", "blog_writing", "content_marketing"
                    - Searches agent names and descriptions for keyword matches

                    ## Multi-Agent Tasks:
                    For complex tasks requiring multiple specialized agents:
                    - Break down into clear subtasks with specific capability needs
                    - Use partial matching to find agents with related skills that can adapt
                    - Check if single versatile agent can handle multiple subtasks (prefer when possible)
                    - Organize results by role/subtask with integration considerations

                    ## Example Multi-Agent Scenarios:
                    - **Website Creation**: Design + Content + SEO + Testing agents
                    - **Data Pipeline**: Collection + Processing + Visualization + Reporting agents
                    - **Marketing Campaign**: Research + Content + Social Media + Analytics agents

                    ## Response Format:
                    **Single-Agent Tasks**: 3-5 ranked recommendations with complete details
                    **Multi-Agent Tasks**: 2-3 top recommendations per subtask, organized by role
                    **Match Types**: Clearly indicate exact matches vs partial matches and explain capability relationships

                    ## Key Principles:
                    - **Partial matching by default** - Find related agents even without exact capability matches
                    - **Exact matches prioritized** - Higher ranking for precise capability matches
                    - **Never return empty results** - Always try progressive search broadening
                    - **Efficiency first** - Prefer single agents when they can handle multiple subtasks
                    - **Clear communication** - Explain search strategy, match types, and reasoning
                    - **Quality over quantity** - Focus on best matches rather than exhaustive lists

                    Hand off to root agent when task is unclear or after presenting agent recommendations.
            """,
    tools=[
        comprehensive_agent_search,
        get_agent_by_id,  
        get_top_agents_by_capability,
        get_best_value_agents
    ],
)
