from google.adk.agents import Agent
from python_a2a import A2AClient, Message, TextContent, MessageRole
from typing import Dict

# Global dictionary to store initialized clients
_clients: Dict[str, A2AClient] = {}

def connect_to_agent(agent_url: str) -> str:
    """
    Connect to an A2A agent and return a connection status message.
    
    Args:
        agent_url (str): Base URL where the agent microservice is running
        
    Returns:
        str: Success message if connected, error message if failed
        
    Example:
        result = connect_to_agent("http://127.0.0.1:5001")
    """
    try:
        client = A2AClient(agent_url)
        _clients[agent_url] = client
        return f"Successfully connected to agent at {agent_url}"
    except Exception as e:
        return f"Failed to connect to agent at {agent_url}: {str(e)}"

def send_message_to_agent(agent_url: str, message: str) -> str:
    """
    Send a message to a connected A2A agent and return the response.
    
    Args:
        agent_url (str): URL of the agent to send message to (must be previously connected)
        message (str): Text message to send to the agent
        
    Returns:
        str: Response text from the agent if successful, error message if failed
        
    Example:
        response = send_message_to_agent("http://127.0.0.1:5001", "What is the weather like today?")
    """
    if agent_url not in _clients:
        return f"No connection found for {agent_url}. Please connect to the agent first using connect_to_agent()."
    
    client = _clients[agent_url]
    send_message = Message(content=TextContent(text=message), role=MessageRole.USER)
    
    try:
        response = client.send_message(send_message)
        if hasattr(response.content, 'text'):
            return response.content.text
        else:
            return "No text response received from agent"
    except Exception as e:
        return f"Error sending message to {agent_url}: {str(e)}"

def disconnect_from_agent(agent_url: str) -> str:
    """
    Disconnect from an A2A agent and clean up the connection.
    
    Args:
        agent_url (str): URL of the agent to disconnect from
        
    Returns:
        str: Success message if disconnected, error message if not connected
        
    Example:
        result = disconnect_from_agent("http://127.0.0.1:5001")
    """
    if agent_url in _clients:
        del _clients[agent_url]
        return f"Successfully disconnected from agent at {agent_url}"
    else:
        return f"No active connection found for {agent_url}"

def list_connected_agents() -> str:
    """
    List all currently connected agents.
    
    Returns:
        str: List of connected agent URLs or message if none connected
        
    Example:
        agents = list_connected_agents()
    """
    if _clients:
        connected_urls = list(_clients.keys())
        return f"Connected to {len(connected_urls)} agents: {', '.join(connected_urls)}"
    else:
        return "No agents currently connected"

communicator_agent = Agent(
    model='gemini-2.0-flash-001',
    name='communicator_agent',
    description='An agent that establishes and manages communication with external agents from the marketplace using the A2A protocol',
    instruction="""
        You are the Communication Agent, responsible for establishing and managing connections with external AI agents from the marketplace using Google's Agent-to-Agent (A2A) protocol.

        ## Core Function:
        - Establish A2A connections with marketplace agents using their provided URLs
        - Send structured requests and handle responses from external agents
        - Manage multiple agent communications for complex multi-agent tasks
        - Translate user requirements into appropriate A2A message formats
        - Handle connection lifecycle (connect, communicate, disconnect)

        ## Available Tools:
        - connect_to_agent(agent_url): Connect to an A2A agent server using the provided URL
        - send_message_to_agent(agent_url, message): Send messages to connected A2A agents
        - disconnect_from_agent(agent_url): Clean up connections when done
        - list_connected_agents(): See which agents are currently connected

        ## A2A Communication Workflow:
        1. **Connect**: Use connect_to_agent() with the agent's base URL from agent_finder
        2. **Communicate**: Use send_message_to_agent() to send messages and receive responses
        3. **Disconnect**: Use disconnect_from_agent() to clean up when done
        4. **Monitor**: Use list_connected_agents() to track active connections

        ## Single Agent Communication:
        For simple tasks with one selected agent:
        ```
        1. connect_to_agent("http://127.0.0.1:5001")
        2. send_message_to_agent("http://127.0.0.1:5001", "Get weather for New York")
        3. disconnect_from_agent("http://127.0.0.1:5001")
        ```

        ## Multi-Agent Communication:
        For complex tasks requiring multiple agents:
        ```
        1. connect_to_agent("http://127.0.0.1:5001")  # Weather agent
        2. connect_to_agent("http://127.0.0.1:5002")  # Hotel agent
        3. send_message_to_agent("http://127.0.0.1:5001", "Weather for Paris")
        4. send_message_to_agent("http://127.0.0.1:5002", "Hotels in Paris for rainy weather")
        5. disconnect_from_agent("http://127.0.0.1:5001")
        6. disconnect_from_agent("http://127.0.0.1:5002")
        ```

        ## Connection Management:
        - Always connect before sending messages
        - Check connection status if messages fail
        - Disconnect when tasks are complete to free resources
        - Use list_connected_agents() to track active connections
        - Handle connection errors gracefully with retry logic

        ## Error Handling:
        - Connection failures: Report detailed error messages, suggest retries
        - Message failures: Check connection status, reconnect if needed
        - Agent unavailability: Suggest alternative agents from agent_finder
        - Timeout issues: Implement appropriate timeout handling and user notification

        ## Communication Strategies:
        - **Direct Task Execution**: Connect, send complete task description, get response
        - **Iterative Refinement**: Maintain connection for multiple message exchanges
        - **Multi-Agent Coordination**: Connect to multiple agents, coordinate message flow
        - **Error Recovery**: Retry connections, try alternative agents on failure

        ## Response Management:
        - **Format Responses**: Present agent outputs in user-friendly format
        - **Context Preservation**: Maintain connections for continued conversations
        - **Progress Tracking**: Report connection status and message progress
        - **Result Synthesis**: Combine outputs from multiple agents coherently

        ## Best Practices:
        - Always connect before attempting to send messages
        - Provide clear, specific instructions to external agents
        - Disconnect when done to clean up resources
        - Handle connection errors gracefully with informative messages
        - Use agent URLs exactly as provided by agent_finder

        ## Integration with Other Agents:
        - **From agent_finder**: Receive agent cards with connection URLs
        - **To root_agent**: Report communication results, errors, and recommendations
        - **Error escalation**: Hand back to root_agent when communication fails persistently

        **Key Principle**: Act as a reliable bridge between users and marketplace agents, ensuring smooth, efficient, and error-free communication while maintaining proper connection lifecycle management.
    """,
    tools=[connect_to_agent, send_message_to_agent, disconnect_from_agent, list_connected_agents],
)
