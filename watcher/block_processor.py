from core.mcp_client import MCPClient
from watcher.transaction_analyzer import TransactionAnalyzer
from watcher.whale_tracker import WhaleTracker
from watcher.balance_monitor import BalanceMonitor
from core.utils import format_whale_event
from config.settings import BALANCE_MONITORING_ENABLED, BALANCE_CHECK_INTERVAL_BLOCKS

class BlockProcessor:
    def __init__(self, mcp_client: MCPClient):
        self.mcp_client = mcp_client
        self.transaction_analyzer = TransactionAnalyzer()
        self.whale_tracker = WhaleTracker()
        self.balance_monitor = BalanceMonitor(mcp_client)
        self.last_block_number = None
        self.blocks_since_balance_check = 0
    
    async def get_latest_block_number(self):
        latest_block_data = await self.mcp_client.get_latest_block()
        return int(latest_block_data["number"])
    
    async def process_block(self, block_number):
        print(f"Processing block: {block_number}")
        block_data = await self.mcp_client.get_block_by_number(block_number)
        tx_hashes = block_data.get("transactions", [])
        
        all_transfers = []
        whale_events = []
        for tx_hash in tx_hashes:
            receipt_data = await self.mcp_client.get_transaction_receipt(tx_hash)
            logs = receipt_data.get("logs", [])
            transfers = self.transaction_analyzer.analyze_transaction_logs(logs, tx_hash)
            all_transfers.extend(transfers)
            
            for transfer in transfers:
                whale_event = self.whale_tracker.analyze_transfer(transfer)
                if whale_event:
                    whale_events.append(whale_event)
                    print(format_whale_event(whale_event))
                    
                    if BALANCE_MONITORING_ENABLED:
                        self.balance_monitor.add_wallet_to_monitor(transfer['from_address'])
                        self.balance_monitor.add_wallet_to_monitor(transfer['to_address'])
        
        return all_transfers, whale_events
    
    async def process_new_blocks(self):
        current_block = await self.get_latest_block_number()
        print("Latest block number:", current_block)
        
        if self.last_block_number is None:
            self.last_block_number = current_block - 1
        
        all_transfers = []
        all_whale_events = []
        for block_num in range(self.last_block_number + 1, current_block + 1):
            transfers, whale_events = await self.process_block(block_num)
            all_transfers.extend(transfers)
            all_whale_events.extend(whale_events)
            
            if BALANCE_MONITORING_ENABLED:
                blocks_processed = current_block - (self.last_block_number or current_block - 1)
                self.blocks_since_balance_check += blocks_processed
                
                if self.blocks_since_balance_check >= BALANCE_CHECK_INTERVAL_BLOCKS:
                    await self._check_monitored_balances()
                    self.blocks_since_balance_check = 0
            
                self.balance_monitor.clear_old_data()
        
        self.last_block_number = current_block
        self.whale_tracker.clear_old_events()
        
        
        
        return all_transfers, all_whale_events
    
    async def _check_monitored_balances(self):
        print("Checking balances for monitored wallets...")
        balance_updates = await self.balance_monitor.check_all_monitored_wallets()
        
        for balance_info in balance_updates:
            balance = balance_info["balance"]
            wallet = balance_info["wallet_address"]
            if balance > 0:
                print(f"Balance update: {wallet[:10]}... has {balance:,.2f} USDC")