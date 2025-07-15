from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import json
from mcp.types import TextContent

# Use npx to run the Sei MCP server
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@sei-js/mcp-server"],
    env=None,  # Or add environment variables like private keys
)

STABLECOIN_ADDRESSES = {
    "USDC": "0x3894085ef7ff0f0aedf52e2a2704928d1ec074f1",
}

async def watcher_agent(session: ClientSession):
    last_block_number = None
    while True:
        latest_block = await session.call_tool("get_latest_block", arguments={"network": "sei"})
        text_content = TextContent.model_validate(latest_block.content[0]).text
        latest_block_data = json.loads(text_content)
        block_number = int(latest_block_data["number"])
        print("Latest block number:", block_number)

        # Only process new blocks
        if last_block_number is None:
            last_block_number = block_number - 1  # Start from previous block

        for bn in range(last_block_number + 1, block_number + 1):
            print(f"Processing block: {bn}")
            block_by_number = await session.call_tool("get_block_by_number", arguments={"blockNumber": bn, "network": "sei"})
            block_by_number_text = TextContent.model_validate(block_by_number.content[0]).text
            block_by_number_data = json.loads(block_by_number_text)
            tx_hashes = block_by_number_data.get("transactions", [])

            for tx_hash in tx_hashes:
                receipt = await session.call_tool(
                    "get_transaction_receipt",
                    arguments={"txHash": tx_hash, "network": "sei"}
                )
                receipt_text = TextContent.model_validate(receipt.content[0]).text
                receipt_data = json.loads(receipt_text)
                logs = receipt_data.get("logs", [])
                for log in logs:
                    if log.get("address", "").lower() in (addr.lower() for addr in STABLECOIN_ADDRESSES.values()):
                        from_addr = "0x" + log["topics"][1][-40:]
                        to_addr = "0x" + log["topics"][2][-40:]
                        value = int(log["data"], 16) / 10**6  # USDC has 6 decimals
                        print(f"""
Stablecoin Transfer Detected!
Tx Hash:   {tx_hash}
Value:     {value} USDC
Block:     {log['blockNumber']}
LogIndex:  {log['logIndex']}
{'-'*40}
                        """)
        last_block_number = block_number
        await asyncio.sleep(5)  # Poll interval

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            await watcher_agent(session)


if __name__ == "__main__":
    asyncio.run(run())