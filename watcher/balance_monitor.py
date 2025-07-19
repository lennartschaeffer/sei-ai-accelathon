from typing import Dict, List, Optional
from datetime import datetime
from core.mcp_client import MCPClient
from config.settings import STABLECOIN_ADDRESSES, USDC_DECIMALS

class BalanceMonitor:
    def __init__(self, mcp_client: MCPClient):
        self.mcp_client = mcp_client
        self.monitored_wallets = set()
        self.wallet_balances = {}
        self.balance_alerts = []
        
    def add_wallet_to_monitor(self, wallet_address: str):
        self.monitored_wallets.add(wallet_address.lower())
    
    def remove_wallet_from_monitor(self, wallet_address: str):
        self.monitored_wallets.discard(wallet_address.lower())
    
    async def check_wallet_balance(self, wallet_address: str, token_address: str) -> Optional[Dict]:
        try:
            balance_data = await self.mcp_client.get_token_balance(wallet_address, token_address)
            balance = float(balance_data.get("formatted", 0))
            
            current_time = datetime.now()
            balance_info = {
                "wallet_address": wallet_address,
                "token_address": token_address,
                "balance": balance,
                "timestamp": current_time
            }
            
            self.wallet_balances[wallet_address] = balance_info
            return balance_info
            
        except Exception as e:
            print(f"Error checking balance for {wallet_address}: {e}")
            return None
    
    async def check_all_monitored_wallets(self):
        usdc_address = STABLECOIN_ADDRESSES["USDC"]
        balance_updates = []
        
        for wallet_address in self.monitored_wallets:
            balance_info = await self.check_wallet_balance(wallet_address, usdc_address)
            if balance_info:
                balance_updates.append(balance_info)
        
        return balance_updates
    
    def get_wallet_balance(self, wallet_address: str) -> Optional[Dict]:
        return self.wallet_balances.get(wallet_address.lower())
    
    def get_all_balances(self) -> Dict:
        return self.wallet_balances.copy()
    
    def clear_old_data(self, keep_last: int = 100):
        if len(self.balance_alerts) > keep_last:
            self.balance_alerts = self.balance_alerts[-keep_last:]