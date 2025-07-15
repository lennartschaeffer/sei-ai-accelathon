from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Use npx to run the Sei MCP server
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@sei-js/mcp-server"],
    env=None,  # Or add environment variables like private keys
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            print("Available Sei tools:")
            for tool in tools_result.tools:
                print(f"- {tool.name}: {tool.description}")

            # # Example: get_supported_networks
            # result = await session.call_tool("get_supported_networks", arguments={})
            # print("Supported networks:", result)

            # # Example: get_token_balance
            # result = await session.call_tool(
            #     "get_token_balance",
            #     arguments={
            #         "tokenAddress": "0x3894085ef7ff0f0aedf52e2a2704928d1ec074f1",
            #         "ownerAddress": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
            #         "network": "sei"
            #     }
            # )
            # print("Token balance result:", result)

            # # Example: get_chain_info
            # result = await session.call_tool(
            #     "get_chain_info",
            #     arguments={"network": "sei"}
            # )
            # print("Chain info:", result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())