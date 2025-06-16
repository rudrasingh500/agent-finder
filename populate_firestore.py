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
    """Returns a list of three specific agents: weather, hotel, and activity recommendation agents."""
    return [
        {
            "agent_id": "weather-agent-v1",
            "agent_name": "Weather Agent",
            "description": "Provides comprehensive weather information for cities worldwide including current conditions, forecasts, and weather alerts.",
            "capabilities": ["weather_information", "weather_forecasting", "location_services", "api_integration"],
            "agent_url": "http://127.0.0.1:5001",
            "agent_pricing": 0.05,  # tokens per request
            "karma": 2100
        },
        {
            "agent_id": "hotel-recommendation-agent-v1",
            "agent_name": "Hotel Recommendation Agent",
            "description": "Recommends hotels based on location and weather conditions, providing personalized accommodation suggestions with pricing and availability.",
            "capabilities": ["hotel_recommendations", "location_services", "weather_integration", "booking_assistance"],
            "agent_url": "http://127.0.0.1:5002",
            "agent_pricing": 0.08,  # tokens per request
            "karma": 1850
        },
        {
            "agent_id": "activity-recommendation-agent-v1",
            "agent_name": "Activity Recommendation Agent",
            "description": "Suggests activities based on location, weather, and accommodation preferences, helping users plan the perfect itinerary.",
            "capabilities": ["activity_recommendations", "itinerary_planning", "weather_integration", "location_services"],
            "agent_url": "http://localhost:5003/a2a",
            "agent_pricing": 0.06,  # tokens per request
            "karma": 1950
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
    # Define specific skills for each agent based on their capabilities
    agent_id = agent_data.get("agent_id", "")
    
    if "weather-agent" in agent_id:
        skills = [{
            "id": "getWeather-1",
            "name": "getWeather",
            "description": "Get weather for a city including current conditions, forecasts, and alerts",
            "tags": ["weather", "forecast", "location", "climate"],
            "examples": [
                "Get current weather conditions for New York City",
                "Provide 7-day weather forecast for London with precipitation details"
            ],
            "inputModes": ["application/json", "text/plain"],
            "outputModes": ["application/json", "text/plain"]
        }]
        provider_org = "Weather AI Solutions"
        
    elif "hotel-recommendation" in agent_id:
        skills = [{
            "id": "findHotels-1",
            "name": "findHotels",
            "description": "Find hotels in a specified location considering weather conditions and user preferences",
            "tags": ["hotels", "accommodation", "booking", "weather-aware", "recommendations"],
            "examples": [
                "Find hotels in Paris for rainy weather with indoor amenities",
                "Recommend beach hotels in Miami with weather-appropriate facilities"
            ],
            "inputModes": ["application/json", "text/plain"],
            "outputModes": ["application/json", "text/plain"]
        }]
        provider_org = "Hotel AI Solutions"
        
    elif "activity-recommendation" in agent_id:
        skills = [{
            "id": "suggestActivities-1",
            "name": "suggestActivities",
            "description": "Suggest activities for a location based on weather and accommodation preferences",
            "tags": ["activities", "itinerary", "weather-based", "location", "planning"],
            "examples": [
                "Suggest indoor activities in Seattle during rainy season",
                "Recommend outdoor activities in San Diego with sunny weather forecast"
            ],
            "inputModes": ["application/json", "text/plain"],
            "outputModes": ["application/json", "text/plain"]
        }]
        provider_org = "Activity AI Solutions"
    else:
        # Fallback for unknown agents
        skills = [{
            "id": "general-1",
            "name": "generalService",
            "description": "Provides general AI services",
            "tags": ["general", "ai", "service"],
            "examples": ["Provide general assistance"],
            "inputModes": ["application/json", "text/plain"],
            "outputModes": ["application/json", "text/plain"]
        }]
        provider_org = "AI Solutions"
    
    # Generate agent name and provider info
    agent_name = agent_data.get("agent_name", "Unknown Agent")
    base_url = agent_data.get("agent_url", "http://localhost:8000")
    provider_url = f"https://{agent_id}.agentmarketplace.com"
    
    # Create the agent card
    agent_card = {
        "name": agent_name,
        "description": agent_data.get("description", "AI agent providing specialized services"),
        "url": base_url,
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
        print("\n📋 DEPLOYED AGENTS:")
        print("   1. Weather Agent - http://127.0.0.1:5001")
        print("      Skills: getWeather (weather information and forecasts)")
        print("      Capabilities: weather_information, weather_forecasting, location_services")
        print("\n   2. Hotel Recommendation Agent - http://127.0.0.1:5002")
        print("      Skills: findHotels (weather-aware hotel recommendations)")
        print("      Capabilities: hotel_recommendations, location_services, weather_integration")
        print("\n   3. Activity Recommendation Agent - http://localhost:5003/a2a")
        print("      Skills: suggestActivities (location and weather-based activity planning)")
        print("      Capabilities: activity_recommendations, itinerary_planning, weather_integration")
        print("\n📋 Database Structure:")
        print("   - agent_id: Unique identifier for the agent")
        print("   - agent_name: Human-readable name of the agent")
        print("   - description: Description of what the agent does")
        print("   - capabilities: Array of agent capabilities")
        print("   - agent_url: A2A protocol URL for connection")
        print("   - agent_pricing: Token-based pricing (tokens per request)")
        print("   - karma: Reddit-style karma score")
        print("   - agent_cards (sub-collection): Google agent2agent protocol formatted cards")
        print("     └── card: Full agent card with skills, capabilities, security, etc.")
        print("\n📋 NEXT STEPS:")
        print("1. Start your agent servers:")
        print("   - Weather Agent: http://127.0.0.1:5001")
        print("   - Hotel Agent: http://127.0.0.1:5002")
        print("   - Activity Agent: http://localhost:5003/a2a")
        print("\n2. Test agent communication through the marketplace")
        print("\n3. Common Search Query Examples:")
        print("   - Find weather agents: where('capabilities', 'array-contains', 'weather_information')")
        print("   - Find hotel agents: where('capabilities', 'array-contains', 'hotel_recommendations')")
        print("   - Find activity agents: where('capabilities', 'array-contains', 'activity_recommendations')")
        print("   - Agent cards: agents/{agent_id}/agent_cards/card")
        print("\n✅ Your agent marketplace with A2A protocol support is ready!")
        print("-----------------------------------------")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please ensure your Firebase credentials are set up correctly.")

if __name__ == "__main__":
    populate_firestore() 