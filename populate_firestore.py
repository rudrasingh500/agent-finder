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

def populate_firestore():
    """
    Uploads sample agent data to Firestore with simplified structure.
    """
    try:
        initialize_services()
        db = firestore.client()
        agents_collection = db.collection('agents')

        sample_agents = get_sample_agents()
        print(f"\nFound {len(sample_agents)} sample agents to process.")

        for agent_data in sample_agents:
            print(f"\nProcessing agent: {agent_data['agent_id']}...")
            
            # Upload the agent document to Firestore
            doc_ref = agents_collection.document(agent_data['agent_id'])
            doc_ref.set(agent_data)
            
            print(f"-> Successfully uploaded '{agent_data['agent_id']}' to Firestore.")

        print("\n-----------------------------------------")
        print("✅ All sample agents have been populated in Firestore with simplified structure.")
        print("\n📋 Database Structure:")
        print("   - agent_id: Unique identifier for the agent")
        print("   - agent_name: Human-readable name of the agent")
        print("   - description: Description of what the agent does")
        print("   - capabilities: Array of agent capabilities")
        print("   - agent_url: Agent2Agent protocol URL for connection")
        print("   - agent_pricing: Token-based pricing (tokens per request)")
        print("   - karma: Reddit-style karma score (150-2500)")
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
        print("\n2. Firebase Console Commands:")
        print("   # Single field indices")
        print("   gcloud firestore indexes fields create --field-path=karma --order=DESCENDING")
        print("   gcloud firestore indexes fields create --field-path=agent_pricing --order=ASCENDING") 
        print("   gcloud firestore indexes fields create --field-path=agent_name --order=ASCENDING")
        print("   gcloud firestore indexes fields create --field-path=capabilities --array-config")
        print("\n   # Composite indices")
        print("   gcloud firestore indexes composite create --project=agent-marketplace-c93af \\")
        print("     --collection-group=agents \\")
        print("     --field-config=field-path=capabilities,array-config=CONTAINS \\")
        print("     --field-config=field-path=karma,order=DESCENDING")
        print("\n   gcloud firestore indexes composite create --project=agent-marketplace-c93af \\")
        print("     --collection-group=agents \\")
        print("     --field-config=field-path=capabilities,array-config=CONTAINS \\")
        print("     --field-config=field-path=agent_pricing,order=ASCENDING")
        print("\n   gcloud firestore indexes composite create --project=agent-marketplace-c93af \\")
        print("     --collection-group=agents \\")
        print("     --field-config=field-path=karma,order=DESCENDING \\")
        print("     --field-config=field-path=agent_pricing,order=ASCENDING")
        print("\n3. Common Search Query Examples:")
        print("   - Find data analysis agents: where('capabilities', 'array-contains', 'data_analysis')")
        print("   - Budget agents: where('agent_pricing', '<=', 0.10)")
        print("   - Top rated: orderBy('karma', 'desc').limit(10)")
        print("   - Best value data agents: where('capabilities', 'array-contains', 'data_analysis')")
        print("                            .orderBy('karma', 'desc').orderBy('agent_pricing', 'asc')")
        print("\n4. ⚠️  TEXT SEARCH LIMITATION:")
        print("   - Firestore doesn't support full-text search on 'description' field")
        print("   - Consider: Algolia, Elasticsearch, or Cloud Search for description search")
        print("   - Alternative: Use client-side filtering for simple description searches")
        print("\n✅ Your agent marketplace search infrastructure is ready!")
        print("-----------------------------------------")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please ensure your Firebase credentials are set up correctly.")

if __name__ == "__main__":
    populate_firestore() 