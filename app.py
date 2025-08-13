import asyncio
from dotenv import load_dotenv
from mcp_use import MCPAgent, MCPClient 
from langchain_google_genai import ChatGoogleGenerativeAI
import os

async def run_memory_chat():
    """Run a chat using MCPAgent's built-in conversation memory"""
    # Load environment variables for API keys
    load_dotenv()
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

    # Config file path - Change this to your config file path
    config_file = "browser_mcp.json" 

    print("Initializing chat...")

    # Create MCP Client and agent with memory enabled.
    client = MCPClient.from_config_file(config_file)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

    # Create agent with memory_enabled set to True.
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True, # Enable built-in conversation memory.
    )

    print("\n====== Interactive MCP Chat ====== ")
    print("Type 'exit' to end the conversation chat.")
    print("==========================\n")

    try:
        # Main loop for interactive chat.
        while True:
            # Get user input.
            user_input = input("\nYou: ")

            # Check for exit command.
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting chat...")
                break

            # Check for clear history command
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleard.")
                continue
            # Get response from agent.
            print("\nAssistant: ",end="", flush=True)

            try:
                # Run the agent with the user input (memory handling is automatic)
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")

    finally:
        # Clean up
        if client and client.sessions:
            await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(run_memory_chat())