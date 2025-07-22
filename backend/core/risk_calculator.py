from typing import Dict, Any, Optional
from core.event_bus import EventPriority
from core.events import RiskIndicators
import logging

logger = logging.getLogger(__name__)

class RiskCalculator:
    def __init__(self):
        self.large_tx_threshold = 100_000
        self.whale_threshold = 1_000_000
        self.significant_balance_change_threshold = 50_000
        self.high_percentage_change_threshold = 0.20  # 20%
    
    def calculate_priority(self, risk_indicators: Dict[str, Any]) -> EventPriority:
        """Calculate event priority based on risk indicators"""
        score = self._calculate_risk_score(risk_indicators)
        
        if score >= 6:
            return EventPriority.CRITICAL
        elif score >= 4:
            return EventPriority.HIGH
        elif score >= 2:
            return EventPriority.MEDIUM
        else:
            return EventPriority.LOW
    
    def _calculate_risk_score(self, indicators: Dict[str, Any]) -> int:
        """Calculate numerical risk score based on multiple factors"""
        score = 0
        
        # Transaction size factor
        transaction_size = indicators.get('transaction_size', 0)
        if transaction_size > self.whale_threshold:
            score += 3
        elif transaction_size > self.large_tx_threshold:
            score += 2
        elif transaction_size > 50_000:
            score += 1
        
        # Wallet volume factor
        wallet_volume = indicators.get('wallet_volume', 0)
        if wallet_volume > 5_000_000:
            score += 3
        elif wallet_volume > 1_000_000:
            score += 2
        elif wallet_volume > 500_000:
            score += 1
        
        # Balance change factor
        balance_change = abs(indicators.get('balance_change', 0))
        if balance_change > 1_000_000:
            score += 3
        elif balance_change > self.significant_balance_change_threshold:
            score += 2
        elif balance_change > 10_000:
            score += 1
        
        # Percentage change factor
        balance_percentage = abs(indicators.get('balance_percentage', 0))
        if balance_percentage > 0.50:  # 50%
            score += 3
        elif balance_percentage > self.high_percentage_change_threshold:
            score += 2
        elif balance_percentage > 0.10:  # 10%
            score += 1
        
        # Event type factor
        event_type = indicators.get('event_type', '')
        if event_type == 'large_transaction':
            score += 1
        elif event_type == 'high_volume':
            score += 2
        
        # Multiple concurrent events factor
        concurrent_events = indicators.get('concurrent_events', 0)
        if concurrent_events > 3:
            score += 3
        elif concurrent_events > 1:
            score += 1
        
        # Combined risk score factor (for multi-factor events)
        combined_risk = indicators.get('combined_risk_score', 0)
        if combined_risk > 7:
            score += 3
        elif combined_risk > 5:
            score += 2
        elif combined_risk > 3:
            score += 1
        
        logger.debug(f"Calculated risk score: {score} from indicators: {indicators}")
        return score
    
    def calculate_whale_priority(self, whale_data: Dict[str, Any]) -> EventPriority:
        """Calculate priority specifically for whale events"""
        indicators = RiskIndicators.from_whale_event(whale_data)
        return self.calculate_priority(indicators)
    
    def calculate_balance_priority(self, balance_data: Dict[str, Any]) -> EventPriority:
        """Calculate priority specifically for balance change events"""
        indicators = RiskIndicators.from_balance_change(balance_data)
        return self.calculate_priority(indicators)
    
    def should_trigger_ai_analysis(self, priority: EventPriority) -> bool:
        """Determine if event priority warrants AI analysis"""
        return priority in [EventPriority.MEDIUM, EventPriority.HIGH, EventPriority.CRITICAL]
    
    def get_monitoring_frequency(self, priority: EventPriority) -> int:
        """Get recommended monitoring frequency in seconds based on priority"""
        frequency_map = {
            EventPriority.CRITICAL: 5,    # 5 seconds
            EventPriority.HIGH: 15,       # 15 seconds
            EventPriority.MEDIUM: 60,     # 1 minute
            EventPriority.LOW: 300        # 5 minutes
        }
        return frequency_map.get(priority, 300)

# Global risk calculator instance
risk_calculator = RiskCalculator()