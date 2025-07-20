from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime
from core.event_bus import EventPriority

@dataclass
class WhaleActivityEventData:
    wallet_address: str
    tx_hash: str
    amount: float
    direction: str
    event_type: str
    total_volume: float
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'wallet_address': self.wallet_address,
            'tx_hash': self.tx_hash,
            'amount': self.amount,
            'direction': self.direction,
            'event_type': self.event_type,
            'total_volume': self.total_volume,
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class LargeTransactionEventData:
    tx_hash: str
    from_address: str
    to_address: str
    value: float
    block_number: int
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'tx_hash': self.tx_hash,
            'from_address': self.from_address,
            'to_address': self.to_address,
            'value': self.value,
            'block_number': self.block_number,
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class BalanceChangeEventData:
    wallet_address: str
    current_balance: float
    previous_balance: Optional[float]
    change_amount: float
    change_percentage: Optional[float]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'wallet_address': self.wallet_address,
            'current_balance': self.current_balance,
            'previous_balance': self.previous_balance,
            'change_amount': self.change_amount,
            'change_percentage': self.change_percentage,
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class MultiFactorEventData:
    risk_factors: Dict[str, Any]
    combined_risk_score: float
    concurrent_events: int
    market_indicators: Optional[Dict[str, Any]]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'risk_factors': self.risk_factors,
            'combined_risk_score': self.combined_risk_score,
            'concurrent_events': self.concurrent_events,
            'market_indicators': self.market_indicators,
            'timestamp': self.timestamp.isoformat()
        }

class EventTypes:
    WHALE_ACTIVITY = "whale_activity"
    LARGE_TRANSACTION = "large_transaction"
    BALANCE_CHANGE = "balance_change"
    MULTI_FACTOR_RISK = "multi_factor_risk"

class RiskIndicators:
    @staticmethod
    def from_whale_event(whale_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert whale event data to risk indicators"""
        return {
            'transaction_size': whale_data.get('amount', 0),
            'wallet_volume': whale_data.get('total_volume', 0),
            'event_type': whale_data.get('event_type', 'unknown'),
            'direction': whale_data.get('direction', 'unknown')
        }
    
    @staticmethod
    def from_balance_change(balance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert balance change data to risk indicators"""
        return {
            'balance_change': balance_data.get('change_amount', 0),
            'balance_percentage': balance_data.get('change_percentage', 0),
            'current_balance': balance_data.get('current_balance', 0)
        }