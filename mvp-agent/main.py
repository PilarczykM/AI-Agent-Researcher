from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import asyncio
from print_styles import get_user_input, print_agent_response, print_error, print_info
from settings import Settings

settings = Settings()

model = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=settings.openai_api_key)

server_params = StdioServerParameters(
    command="npx",
    env={"FIRECRAWL_API_KEY": settings.firecrawl_api_key},
    args=["firecrawl-mcp"],
)


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(tools=tools, model=model)

            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that can scrape websites, crawl pages and extract sata using Firecrawl tools. "
                    "Think step by step and use the appropriate tools to help user.",
                }
            ]

            print_info(f"Available Tools -{[tool.name for tool in tools]}")
            print("-" * 60)

            while True:
                try:
                    user_input = get_user_input()
                except KeyboardInterrupt:
                    print_info("\nGoodbye!")
                    break
                if user_input == "quit":
                    print_info("\nGoodbye")
                    break

                messages.append({"role": "user", "content": user_input[:30000]})

                try:
                    agent_response = await agent.ainvoke({"messages": messages})
                    ai_response = agent_response["messages"][-1].content
                    print_agent_response(ai_response)
                except Exception as e:
                    print_error(str(e))


if __name__ == "__main__":
    asyncio.run(main())
