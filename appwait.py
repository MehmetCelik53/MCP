import asyncio
import time
from dotenv import load_dotenv
from mcp_use import MCPAgent, MCPClient 
from langchain_google_genai import ChatGoogleGenerativeAI
import os

async def run_memory_chat():
    """Run a chat using MCPAgent's built-in conversation memory with rate limiting protection"""
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

    last_request_time = 0
    min_delay = 3  # Minimum 3 seconds between requests

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
                print("Conversation history cleared.")
                continue

            # Rate limiting: ensure minimum delay between requests
            current_time = time.time()
            time_since_last_request = current_time - last_request_time
            
            if time_since_last_request < min_delay:
                wait_time = min_delay - time_since_last_request
                print(f"⏳ Waiting {wait_time:.1f} seconds to avoid rate limiting...")
                await asyncio.sleep(wait_time)

            # Get response from agent.
            print("\nAssistant: ", end="", flush=True)

            # Retry mechanism for rate limiting errors
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Update last request time
                    last_request_time = time.time()
                    
                    # Run the agent with the user input (memory handling is automatic)
                    response = await agent.run(user_input)
                    print(response)
                    break  # Success, exit retry loop

                except Exception as e:
                    error_message = str(e).lower()
                    
                    # Check for rate limiting errors
                    if ("ddg detected an anomaly" in error_message or 
                        "too quickly" in error_message or
                        "rate limit" in error_message):
                        
                        if attempt < max_retries - 1:
                            wait_time = (attempt + 1) * 10  # 10, 20, 30 seconds
                            print(f"\n🚫 Rate limit detected. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            print(f"\n❌ Max retries reached. Error: Rate limiting persists")
                    else:
                        print(f"\n❌ Error: {e}")
                    break

            # Additional delay after each successful request
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n\n🛑 Chat interrupted by user")
    
    finally:
        # Clean up
        try:
            if client and hasattr(client, 'sessions') and client.sessions:
                await client.close_all_sessions()
                print("🧹 Sessions cleaned up")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")


async def run_with_custom_delays():
    """Alternative version with configurable delays"""
    
    # Configuration
    CONFIG = {
        "min_delay_between_requests": 3,  # seconds
        "max_retries": 3,
        "base_retry_delay": 10,  # seconds
        "post_request_delay": 1  # seconds
    }
    
    print(f"📋 Using delays: {CONFIG['min_delay_between_requests']}s between requests, {CONFIG['base_retry_delay']}s retry delay")
    
    # Your existing initialization code here...
    # (Same as above but with CONFIG values)


if __name__ == "__main__":
    # Choose which version to run
    print("🚀 Starting MCP Chat with rate limiting protection...")
    asyncio.run(run_memory_chat())
    
    # Alternative: Run with custom delays
    # asyncio.run(run_with_custom_delays())
