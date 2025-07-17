import json
from mcp import ClientSession
from mcp.types import TextContent
from config.settings import NETWORK

class MCPClient:
    def __init__(self, session: ClientSession):
        self.session = session
    
    async def get_latest_block(self):
        result = await self.session.call_tool("get_latest_block", arguments={"network": NETWORK})
        text_content = TextContent.model_validate(result.content[0]).text
        return json.loads(text_content)
    
    async def get_block_by_number(self, block_number):
        result = await self.session.call_tool(
            "get_block_by_number", 
            arguments={"blockNumber": block_number, "network": NETWORK}
        )
        text_content = TextContent.model_validate(result.content[0]).text
        return json.loads(text_content)
    
    async def get_transaction_receipt(self, tx_hash):
        result = await self.session.call_tool(
            "get_transaction_receipt",
            arguments={"txHash": tx_hash, "network": NETWORK}
        )
        text_content = TextContent.model_validate(result.content[0]).text
        return json.loads(text_content)