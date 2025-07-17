from datetime import datetime, timedelta
from typing import Dict, List, Optional
from config.settings import WHALE_SINGLE_TX_THRESHOLD, WHALE_VOLUME_THRESHOLD, WHALE_TIME_WINDOW_MINUTES

class WhaleTracker:
    def __init__(self):
        self.wallet_activity = {}
        self.whale_events = []
    
    def _clean_old_activity(self, current_time: datetime):
        cutoff_time = current_time - timedelta(minutes=WHALE_TIME_WINDOW_MINUTES)
        
        for wallet in list(self.wallet_activity.keys()):
            self.wallet_activity[wallet] = [
                tx for tx in self.wallet_activity[wallet] 
                if tx['timestamp'] > cutoff_time
            ]
            if not self.wallet_activity[wallet]:
                del self.wallet_activity[wallet]
    
    def _update_wallet_activity(self, wallet_address: str, amount: float, timestamp: datetime, tx_hash: str):
        if wallet_address not in self.wallet_activity:
            self.wallet_activity[wallet_address] = []
        
        self.wallet_activity[wallet_address].append({
            'amount': amount,
            'timestamp': timestamp,
            'tx_hash': tx_hash
        })
    
    def _calculate_wallet_volume(self, wallet_address: str) -> float:
        if wallet_address not in self.wallet_activity:
            return 0.0
        
        return sum(tx['amount'] for tx in self.wallet_activity[wallet_address])
    
    def _create_whale_event(self, wallet_address: str, tx_hash: str, amount: float, 
                           timestamp: datetime, direction: str, event_type: str) -> Dict:
        return {
            'wallet_address': wallet_address,
            'tx_hash': tx_hash,
            'amount': amount,
            'timestamp': timestamp,
            'direction': direction,
            'event_type': event_type,
            'total_volume': self._calculate_wallet_volume(wallet_address)
        }
    
    def analyze_transfer(self, transfer: Dict) -> Optional[Dict]:
        timestamp = datetime.now()
        amount = transfer['value']
        tx_hash = transfer['tx_hash']
        from_address = transfer['from_address']
        to_address = transfer['to_address']
        
        self._clean_old_activity(timestamp)
        
        whale_event = None
        
        self._update_wallet_activity(from_address, amount, timestamp, tx_hash)
        self._update_wallet_activity(to_address, amount, timestamp, tx_hash)
        
        if amount >= WHALE_SINGLE_TX_THRESHOLD:
            whale_event = self._create_whale_event(
                from_address, tx_hash, amount, timestamp, 'outgoing', 'large_transaction'
            )
        else:
            from_volume = self._calculate_wallet_volume(from_address)
            to_volume = self._calculate_wallet_volume(to_address)
            
            if from_volume >= WHALE_VOLUME_THRESHOLD:
                whale_event = self._create_whale_event(
                    from_address, tx_hash, amount, timestamp, 'outgoing', 'high_volume'
                )
            elif to_volume >= WHALE_VOLUME_THRESHOLD:
                whale_event = self._create_whale_event(
                    to_address, tx_hash, amount, timestamp, 'incoming', 'high_volume'
                )
        
        if whale_event:
            self.whale_events.append(whale_event)
        
        return whale_event
    
    def get_recent_whale_events(self, limit: int = 10) -> List[Dict]:
        return self.whale_events[-limit:] if self.whale_events else []
    
    def clear_old_events(self, keep_last: int = 100):
        if len(self.whale_events) > keep_last:
            self.whale_events = self.whale_events[-keep_last:]