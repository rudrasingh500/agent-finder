from google.adk.agents import Agent
from google.adk.tools import google_search

search_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    description="Search agent to help find information on the internet.",
    instruction="""
    You are a helpful assistant that can search the internet for information using the google_search tool.

    The tools you have available are:
    - google_search: Search the internet for information.
    """,
    tools=[google_search],
)