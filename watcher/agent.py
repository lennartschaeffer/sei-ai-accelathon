from mcp import ClientSession
from mcp.client.stdio import stdio_client
import asyncio
from config.settings import SERVER_PARAMS, POLL_INTERVAL
from core.mcp_client import MCPClient
from watcher.block_processor import BlockProcessor

async def watcher_agent(session: ClientSession):
    mcp_client = MCPClient(session)
    block_processor = BlockProcessor(mcp_client)
    
    while True:
        await block_processor.process_new_blocks()
        await asyncio.sleep(POLL_INTERVAL)

async def run():
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            await watcher_agent(session)


if __name__ == "__main__":
    asyncio.run(run())