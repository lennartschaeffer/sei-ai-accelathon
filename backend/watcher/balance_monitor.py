from typing import Dict, List, Optional
from datetime import datetime
from core.mcp_client import MCPClient
from config.settings import STABLECOIN_ADDRESSES, USDC_DECIMALS, EVENT_BUS_ENABLED
import asyncio
import time

class BalanceMonitor:
    def __init__(self, mcp_client: MCPClient):
        self.mcp_client = mcp_client
        self.monitored_wallets = set()
        self.wallet_balances = {}
        self.previous_balances = {}
        self.balance_alerts = []
        self.event_bus = None
        if EVENT_BUS_ENABLED:
            self._initialize_event_bus()
        
    def _initialize_event_bus(self):
        """Initialize event bus connection"""
        try:
            from core.event_bus import event_bus
            from core.risk_calculator import risk_calculator
            self.event_bus = event_bus
            self.risk_calculator = risk_calculator
        except ImportError:
            print("Warning: Event bus not available")
            self.event_bus = None
        
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
            
            # Check for significant balance changes
            previous_balance = self.previous_balances.get(wallet_address)
            if previous_balance is not None and self.event_bus:
                self._check_and_publish_balance_change(wallet_address, balance, previous_balance, current_time)
            
            self.previous_balances[wallet_address] = balance
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
    
    def _check_and_publish_balance_change(self, wallet_address: str, current_balance: float, previous_balance: float, timestamp: datetime):
        """Check for significant balance changes and publish events"""
        try:
            change_amount = current_balance - previous_balance
            change_percentage = abs(change_amount / previous_balance) if previous_balance > 0 else 0
            
            # Only publish if change is significant (>$10k or >10%)
            if abs(change_amount) > 10000 or change_percentage > 0.10:
                from core.events import BalanceChangeEventData, EventTypes
                from core.event_bus import Event
                
                # Create balance change event data
                event_data = BalanceChangeEventData(
                    wallet_address=wallet_address,
                    current_balance=current_balance,
                    previous_balance=previous_balance,
                    change_amount=change_amount,
                    change_percentage=change_percentage,
                    timestamp=timestamp
                )
                
                # Calculate priority using risk calculator
                balance_data = {
                    'balance_change': abs(change_amount),
                    'balance_percentage': change_percentage,
                    'current_balance': current_balance
                }
                priority = self.risk_calculator.calculate_balance_priority(balance_data)
                
                # Create and publish event
                event = Event(
                    event_type=EventTypes.BALANCE_CHANGE,
                    data=event_data.to_dict(),
                    priority=priority,
                    timestamp=time.time()
                )
                
                # Schedule async publish
                asyncio.create_task(self.event_bus.publish(event))
                
        except Exception as e:
            print(f"Error publishing balance change event: {e}")
    
    def clear_old_data(self, keep_last: int = 100):
        if len(self.balance_alerts) > keep_last:
            self.balance_alerts = self.balance_alerts[-keep_last:]