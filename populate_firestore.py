import os
import random
import uuid
import firebase_admin
from firebase_admin import credentials, firestore

def initialize_services():
    """
    Initializes Firebase Admin SDK.
    """
    # Initialize Firebase
    try:
        # Construct an absolute path to the credentials file relative to this script's location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cred_path = os.path.join(script_dir, "agent-marketplace-c93af-a8fcbc1beb09.json")
        
        print(f"Initializing Firebase with credentials from: {cred_path}")

        if not os.path.exists(cred_path):
            raise FileNotFoundError(f"Credential file not found at: {cred_path}")

        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully.")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        raise

def get_sample_agents():
    """Returns a list of diverse, sample agent data with simplified structure."""
    return [
        {
            "agent_id": "data-analysis-pro-v1",
            "agent_name": "Data Analysis Pro",
            "description": "Expert in statistical analysis, data modeling, and generating business intelligence reports. Can handle large datasets efficiently.",
            "capabilities": ["data_analysis", "sql", "business_intelligence", "statistics"],
            "agent_url": "agent2agent://data-analysis-pro-v1.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.01, 0.15), 3),  # tokens per request
            "karma": random.randint(150, 2500)
        },
        {
            "agent_id": "creative-writer-gpt-v2",
            "agent_name": "Creative Writer GPT",
            "description": "Generates high-quality, human-like text for blogs, marketing copy, and scripts. Specializes in creative and engaging content.",
            "capabilities": ["content_creation", "copywriting", "natural_language_generation", "creative_writing"],
            "agent_url": "agent2agent://creative-writer-gpt-v2.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.02, 0.20), 3),
            "karma": random.randint(150, 2500)
        },
        {
            "agent_id": "sentiment-analyzer-v3",
            "agent_name": "Sentiment Analyzer",
            "description": "Analyzes text to determine sentiment (positive, negative, neutral). Ideal for processing customer feedback, social media comments, and product reviews.",
            "capabilities": ["sentiment_analysis", "natural_language_processing", "text_classification"],
            "agent_url": "agent2agent://sentiment-analyzer-v3.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.005, 0.08), 3),
            "karma": random.randint(150, 2500)
        },
        {
            "agent_id": "web-scraper-bot-v4",
            "agent_name": "Web Scraper Bot",
            "description": "Extracts structured and unstructured data from websites. Can handle dynamic pages, logins, and CAPTCHAs.",
            "capabilities": ["web_scraping", "data_collection", "html_parsing", "automation"],
            "agent_url": "agent2agent://web-scraper-bot-v4.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.03, 0.25), 3),
            "karma": random.randint(150, 2500)
        },
        {
            "agent_id": "image-recognition-cnn-v1",
            "agent_name": "Image Recognition CNN",
            "description": "Identifies objects, faces, and scenes in images using advanced Convolutional Neural Networks.",
            "capabilities": ["image_recognition", "computer_vision", "object_detection", "deep_learning"],
            "agent_url": "agent2agent://image-recognition-cnn-v1.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.04, 0.30), 3),
            "karma": random.randint(150, 2500)
        },
        {
            "agent_id": "code-generator-alpha-v1.2",
            "agent_name": "Code Generator Alpha",
            "description": "Generates code snippets in multiple programming languages based on natural language descriptions. Supports Python, JavaScript, and Java.",
            "capabilities": ["code_generation", "python", "javascript", "developer_tools"],
            "agent_url": "agent2agent://code-generator-alpha-v1-2.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.02, 0.18), 3),
            "karma": random.randint(150, 2500)
        },
        {
            "agent_id": "financial-forecaster-v2",
            "agent_name": "Financial Forecaster",
            "description": "Predicts stock market trends, analyzes investment portfolios, and generates financial forecasts using time-series analysis.",
            "capabilities": ["financial_analysis", "forecasting", "investment_management", "time_series"],
            "agent_url": "agent2agent://financial-forecaster-v2.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.05, 0.35), 3),
            "karma": random.randint(150, 2500)
        },
        {
            "agent_id": "customer-support-chatbot-v5",
            "agent_name": "SupportBot 3000",
            "description": "An automated chatbot for handling customer support inquiries, answering FAQs, and escalating complex issues to human agents.",
            "capabilities": ["chatbot", "customer_service", "faq_answering", "dialogue_management"],
            "agent_url": "agent2agent://customer-support-chatbot-v5.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.01, 0.12), 3),
            "karma": random.randint(150, 2500)
        },
        {
            "agent_id": "translation-service-v1",
            "agent_name": "Polyglot Translator",
            "description": "Provides fast and accurate translation between over 50 languages. Maintains context and idiomatic expressions.",
            "capabilities": ["translation", "multilingual", "natural_language_processing"],
            "agent_url": "agent2agent://translation-service-v1.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.01, 0.10), 3),
            "karma": random.randint(150, 2500)
        },
        {
            "agent_id": "research-assistant-v1",
            "agent_name": "Academic Research Assistant",
            "description": "Summarizes academic papers, finds relevant literature, and helps in drafting research proposals.",
            "capabilities": ["text_summarization", "research", "academic_writing", "information_retrieval"],
            "agent_url": "agent2agent://research-assistant-v1.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.02, 0.16), 3),
            "karma": random.randint(150, 2500)
        },
        {
            "agent_id": "music-composer-v1",
            "agent_name": "Maestro AI",
            "description": "Composes original royalty-free music in various genres, from classical to electronic.",
            "capabilities": ["music_generation", "creative_tools", "audio_processing"],
            "agent_url": "agent2agent://music-composer-v1.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.06, 0.40), 3),
            "karma": random.randint(150, 2500)
        },
        {
            "agent_id": "video-analyzer-v1",
            "agent_name": "Video Insights Extractor",
            "description": "Analyzes video content to detect objects, transcribe speech, and identify key scenes.",
            "capabilities": ["video_analysis", "speech_to_text", "computer_vision"],
            "agent_url": "agent2agent://video-analyzer-v1.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.08, 0.50), 3),
            "karma": random.randint(150, 2500)
        },
        {
            "agent_id": "personal-finance-manager-v2",
            "agent_name": "MyFinance Pal",
            "description": "Helps users track expenses, create budgets, and provides personalized financial advice.",
            "capabilities": ["personal_finance", "budgeting", "expense_tracking"],
            "agent_url": "agent2agent://personal-finance-manager-v2.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.01, 0.14), 3),
            "karma": random.randint(150, 2500)
        },
        {
            "agent_id": "game-npc-logic-v1",
            "agent_name": "Game NPC Brain",
            "description": "Provides advanced AI logic for non-player characters in video games, creating dynamic and responsive behaviors.",
            "capabilities": ["game_development", "ai_logic", "npc_behavior"],
            "agent_url": "agent2agent://game-npc-logic-v1.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.03, 0.22), 3),
            "karma": random.randint(150, 2500)
        },
        {
            "agent_id": "social-media-manager-v3",
            "agent_name": "Social Media Growth Manager",
            "description": "Schedules posts, analyzes engagement metrics, and suggests content strategies to grow social media presence.",
            "capabilities": ["social_media_management", "marketing_automation", "analytics"],
            "agent_url": "agent2agent://social-media-manager-v3.agentmarketplace.com/connect",
            "agent_pricing": round(random.uniform(0.02, 0.17), 3),
            "karma": random.randint(150, 2500)
        }
    ]

def generate_agent_card(agent_data):
    """
    Generates an agent card following Google's agent2agent protocol format.
    
    Args:
        agent_data: The original agent data dictionary
    
    Returns:
        Dictionary following agent2agent protocol format
    """
    # Map capabilities to skills with examples
    skills = []
    capability_mapping = {
        "data_analysis": {
            "name": "Data Analysis & Insights",
            "description": "Performs comprehensive data analysis, statistical modeling, and generates actionable business insights from complex datasets.",
            "tags": ["analytics", "statistics", "data", "insights", "reporting"],
            "examples": [
                "Analyze sales data to identify trends and forecast future performance",
                "Perform customer segmentation analysis based on behavioral data"
            ]
        },
        "sql": {
            "name": "SQL Database Operations",
            "description": "Executes complex SQL queries, optimizes database performance, and manages data extraction and transformation tasks.",
            "tags": ["database", "sql", "queries", "data extraction", "optimization"],
            "examples": [
                "Extract customer purchase history from multiple joined tables",
                "Optimize slow-running queries for better performance"
            ]
        },
        "content_creation": {
            "name": "Content Creation & Writing",
            "description": "Creates engaging, high-quality content for various platforms including blogs, social media, marketing materials, and documentation.",
            "tags": ["writing", "content", "marketing", "copywriting", "creative"],
            "examples": [
                "Write a compelling blog post about emerging technology trends",
                "Create engaging social media content for a product launch campaign"
            ]
        },
        "web_scraping": {
            "name": "Web Data Extraction",
            "description": "Extracts structured and unstructured data from websites, handles dynamic content, and manages large-scale data collection operations.",
            "tags": ["scraping", "data collection", "automation", "web", "extraction"],
            "examples": [
                "Extract product prices and reviews from e-commerce websites",
                "Collect real estate listings data from multiple property websites"
            ]
        },
        "image_recognition": {
            "name": "Computer Vision & Image Analysis",
            "description": "Analyzes images and videos to detect objects, recognize faces, classify scenes, and extract visual information using deep learning models.",
            "tags": ["computer vision", "image processing", "object detection", "AI", "machine learning"],
            "examples": [
                "Identify and classify objects in retail inventory photos",
                "Analyze medical images to detect anomalies and assist diagnosis"
            ]
        },
        "code_generation": {
            "name": "Code Generation & Development",
            "description": "Generates high-quality code in multiple programming languages based on natural language specifications and requirements.",
            "tags": ["programming", "code generation", "development", "automation", "software"],
            "examples": [
                "Generate a Python script for data processing based on requirements",
                "Create a React component for user authentication with validation"
            ]
        },
        "financial_analysis": {
            "name": "Financial Analysis & Forecasting",
            "description": "Provides comprehensive financial analysis, market research, investment strategies, and predictive modeling for financial markets.",
            "tags": ["finance", "investment", "forecasting", "analysis", "markets"],
            "examples": [
                "Analyze portfolio performance and suggest optimization strategies",
                "Forecast stock market trends using technical and fundamental analysis"
            ]
        },
        "chatbot": {
            "name": "Conversational AI & Support",
            "description": "Provides intelligent conversational interfaces for customer support, FAQ handling, and automated assistance across multiple channels.",
            "tags": ["chatbot", "customer service", "conversation", "automation", "support"],
            "examples": [
                "Handle customer inquiries and provide instant support responses",
                "Guide users through complex product setup processes"
            ]
        },
        "translation": {
            "name": "Multi-Language Translation",
            "description": "Provides accurate translation services across multiple languages while preserving context, tone, and cultural nuances.",
            "tags": ["translation", "multilingual", "localization", "language", "communication"],
            "examples": [
                "Translate business documents while maintaining professional tone",
                "Localize mobile app content for different regional markets"
            ]
        },
        "text_summarization": {
            "name": "Text Analysis & Summarization",
            "description": "Analyzes large volumes of text to extract key insights, generate summaries, and identify important themes and patterns.",
            "tags": ["summarization", "text analysis", "research", "insights", "processing"],
            "examples": [
                "Summarize lengthy research papers into key findings and conclusions",
                "Extract main points from customer feedback and reviews"
            ]
        }
    }
    
    # Generate skills based on agent capabilities
    for i, capability in enumerate(agent_data.get("capabilities", [])[:3]):  # Limit to 3 skills
        if capability in capability_mapping:
            skill_info = capability_mapping[capability]
            skill = {
                "id": f"{capability}-{i+1}",
                "name": skill_info["name"],
                "description": skill_info["description"],
                "tags": skill_info["tags"],
                "examples": skill_info["examples"],
                "inputModes": ["application/json", "text/plain"],
                "outputModes": ["application/json", "text/plain"]
            }
            skills.append(skill)
    
    # Generate provider organization name
    agent_name = agent_data.get("agent_name", "Unknown Agent")
    provider_org = f"{agent_name.split()[0]} AI Solutions"
    provider_url = f"https://{agent_data.get('agent_id', 'unknown')}.agentmarketplace.com"
    
    # Create the agent card
    agent_card = {
        "name": agent_name,
        "description": agent_data.get("description", "AI agent providing specialized services"),
        "url": agent_data.get("agent_url", f"agent2agent://{agent_data.get('agent_id', 'unknown')}.agentmarketplace.com/connect"),
        "provider": {
            "organization": provider_org,
            "url": provider_url
        },
        "iconUrl": f"{provider_url}/icon.png",
        "version": "1.0.0",
        "documentationUrl": f"{provider_url}/docs",
        "capabilities": {
            "streaming": random.choice([True, False]),
            "pushNotifications": random.choice([True, False]),
            "stateTransitionHistory": random.choice([True, False])
        },
        "securitySchemes": {
            "google": {
                "type": "openIdConnect",
                "openIdConnectUrl": "https://accounts.google.com/.well-known/openid-configuration"
            }
        },
        "security": [{"google": ["openid", "profile", "email"]}],
        "defaultInputModes": ["application/json", "text/plain"],
        "defaultOutputModes": ["application/json", "text/plain"],
        "skills": skills,
        "supportsAuthenticatedExtendedCard": True,
        "pricing": {
            "model": "token_based",
            "cost_per_request": agent_data.get("agent_pricing", 0.1),
            "currency": "tokens"
        },
        "metadata": {
            "karma": agent_data.get("karma", 1000),
            "capabilities_list": agent_data.get("capabilities", []),
            "created_at": "2024-01-01T00:00:00Z",
            "last_updated": "2024-01-01T00:00:00Z"
        }
    }
    
    return agent_card

def populate_firestore():
    """
    Uploads sample agent data to Firestore with simplified structure and agent cards.
    """
    try:
        initialize_services()
        db = firestore.client()
        agents_collection = db.collection('agents')

        sample_agents = get_sample_agents()
        print(f"\nFound {len(sample_agents)} sample agents to process.")

        for agent_data in sample_agents:
            print(f"\nProcessing agent: {agent_data['agent_id']}...")
            
            # Upload the main agent document to Firestore
            doc_ref = agents_collection.document(agent_data['agent_id'])
            doc_ref.set(agent_data)
            
            print(f"-> Successfully uploaded '{agent_data['agent_id']}' to Firestore.")
            
            # Generate and upload agent card as sub-collection
            agent_card = generate_agent_card(agent_data)
            agent_card_ref = doc_ref.collection('agent_cards').document('card')
            agent_card_ref.set(agent_card)
            
            print(f"-> Successfully uploaded agent card for '{agent_data['agent_id']}'.")

        print("\n-----------------------------------------")
        print("✅ All sample agents and agent cards have been populated in Firestore.")
        print("\n📋 Database Structure:")
        print("   - agent_id: Unique identifier for the agent")
        print("   - agent_name: Human-readable name of the agent")
        print("   - description: Description of what the agent does")
        print("   - capabilities: Array of agent capabilities")
        print("   - agent_url: Agent2Agent protocol URL for connection")
        print("   - agent_pricing: Token-based pricing (tokens per request)")
        print("   - karma: Reddit-style karma score (150-2500)")
        print("   - agent_cards (sub-collection): Google agent2agent protocol formatted cards")
        print("     └── card: Full agent card with skills, capabilities, security, etc.")
        print("\n📋 NEXT STEPS:")
        print("1. Create Firebase indices for effective search:")
        print("\n   🔍 SINGLE FIELD INDICES (for basic filtering/sorting):")
        print("   - karma (DESCENDING) - for reputation-based sorting")
        print("   - agent_pricing (ASCENDING) - for price-based filtering")
        print("   - agent_name (ASCENDING) - for name-based searches")
        print("\n   🔍 ARRAY-CONTAINS INDICES (for capability searches):")
        print("   - capabilities (ARRAY_CONTAINS) - for finding specific skills")
        print("\n   🔍 COMPOSITE INDICES (for multi-field queries):")
        print("   - capabilities + karma (DESC) - popular agents with specific skills")
        print("   - capabilities + agent_pricing (ASC) - cheapest agents with specific skills")
        print("   - karma (DESC) + agent_pricing (ASC) - best value agents")
        print("\n2. Agent Card Features:")
        print("   - Google agent2agent protocol compliant")
        print("   - Skills mapped from capabilities with examples")
        print("   - Security schemes and authentication")
        print("   - Streaming and notification capabilities")
        print("   - Comprehensive metadata and documentation")
        print("\n3. Common Search Query Examples:")
        print("   - Find data analysis agents: where('capabilities', 'array-contains', 'data_analysis')")
        print("   - Budget agents: where('agent_pricing', '<=', 0.10)")
        print("   - Top rated: orderBy('karma', 'desc').limit(10)")
        print("   - Agent cards: agents/{agent_id}/agent_cards/card")
        print("\n✅ Your agent marketplace with agent2agent protocol support is ready!")
        print("-----------------------------------------")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please ensure your Firebase credentials are set up correctly.")

if __name__ == "__main__":
    populate_firestore() 