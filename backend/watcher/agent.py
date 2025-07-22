import asyncio
from config.settings import POLL_INTERVAL, SEI_RPC_URL
from core.rpc_client import RPCClient
from watcher.block_processor import BlockProcessor

async def watcher_agent():
    async with RPCClient(SEI_RPC_URL) as rpc_client:
        block_processor = BlockProcessor(rpc_client)
    
        # Start event bus processing
        await block_processor.start_event_processing()
        
        try:
            while True:
                await block_processor.process_new_blocks()
                await asyncio.sleep(POLL_INTERVAL)
        finally:
            # Clean up event bus processing
            await block_processor.stop_event_processing()

async def run():
    await watcher_agent()


if __name__ == "__main__":
    asyncio.run(run())