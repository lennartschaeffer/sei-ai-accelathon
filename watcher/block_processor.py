from core.mcp_client import MCPClient
from watcher.transaction_analyzer import TransactionAnalyzer

class BlockProcessor:
    def __init__(self, mcp_client: MCPClient):
        self.mcp_client = mcp_client
        self.transaction_analyzer = TransactionAnalyzer()
        self.last_block_number = None
    
    async def get_latest_block_number(self):
        latest_block_data = await self.mcp_client.get_latest_block()
        return int(latest_block_data["number"])
    
    async def process_block(self, block_number):
        print(f"Processing block: {block_number}")
        block_data = await self.mcp_client.get_block_by_number(block_number)
        tx_hashes = block_data.get("transactions", [])
        
        all_transfers = []
        for tx_hash in tx_hashes:
            receipt_data = await self.mcp_client.get_transaction_receipt(tx_hash)
            logs = receipt_data.get("logs", [])
            transfers = self.transaction_analyzer.analyze_transaction_logs(logs, tx_hash)
            all_transfers.extend(transfers)
        
        return all_transfers
    
    async def process_new_blocks(self):
        current_block = await self.get_latest_block_number()
        print("Latest block number:", current_block)
        
        if self.last_block_number is None:
            self.last_block_number = current_block - 1
        
        all_transfers = []
        for block_num in range(self.last_block_number + 1, current_block + 1):
            transfers = await self.process_block(block_num)
            all_transfers.extend(transfers)
        
        self.last_block_number = current_block
        return all_transfers