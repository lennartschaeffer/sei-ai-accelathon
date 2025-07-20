import logging
from datetime import datetime
from typing import Dict, Any
from core.event_bus import Event, EventPriority
from core.events import EventTypes

logger = logging.getLogger(__name__)

class MockAIAgent:
    """Mock AI agent for testing event flow in Phase 1"""
    
    def __init__(self):
        self.processed_events = []
        self.event_count = {
            EventTypes.WHALE_ACTIVITY: 0,
            EventTypes.BALANCE_CHANGE: 0,
            EventTypes.LARGE_TRANSACTION: 0,
            EventTypes.MULTI_FACTOR_RISK: 0
        }
    
    async def handle_whale_activity(self, event: Event):
        """Handle whale activity events"""
        self.event_count[EventTypes.WHALE_ACTIVITY] += 1
        self.processed_events.append(event)
        
        data = event.data
        wallet = data.get('wallet_address', 'unknown')[:10]
        amount = data.get('amount', 0)
        event_type = data.get('event_type', 'unknown')
        
        print(f"[MOCK AI] Whale Activity Detected:")
        print(f"  Priority: {event.priority.name}")
        print(f"  Wallet: {wallet}...")
        print(f"  Amount: ${amount:,.2f}")
        print(f"  Type: {event_type}")
        print(f"  Risk Assessment: {self._generate_mock_assessment(event.priority)}")
        print()
    
    async def handle_balance_change(self, event: Event):
        """Handle balance change events"""
        self.event_count[EventTypes.BALANCE_CHANGE] += 1
        self.processed_events.append(event)
        
        data = event.data
        wallet = data.get('wallet_address', 'unknown')[:10]
        change_amount = data.get('change_amount', 0)
        change_percentage = data.get('change_percentage', 0)
        
        print(f"[MOCK AI] Balance Change Detected:")
        print(f"  Priority: {event.priority.name}")
        print(f"  Wallet: {wallet}...")
        print(f"  Change: ${change_amount:,.2f} ({change_percentage:.1%})")
        print(f"  Risk Assessment: {self._generate_mock_assessment(event.priority)}")
        print()
    
    async def handle_large_transaction(self, event: Event):
        """Handle large transaction events"""
        self.event_count[EventTypes.LARGE_TRANSACTION] += 1
        self.processed_events.append(event)
        
        data = event.data
        tx_hash = data.get('tx_hash', 'unknown')[:10]
        value = data.get('value', 0)
        
        print(f"[MOCK AI] Large Transaction Detected:")
        print(f"  Priority: {event.priority.name}")
        print(f"  TX: {tx_hash}...")
        print(f"  Value: ${value:,.2f}")
        print(f"  Risk Assessment: {self._generate_mock_assessment(event.priority)}")
        print()
    
    async def handle_multi_factor_risk(self, event: Event):
        """Handle multi-factor risk events"""
        self.event_count[EventTypes.MULTI_FACTOR_RISK] += 1
        self.processed_events.append(event)
        
        data = event.data
        risk_score = data.get('combined_risk_score', 0)
        concurrent_events = data.get('concurrent_events', 0)
        
        print(f"[MOCK AI] Multi-Factor Risk Detected:")
        print(f"  Priority: {event.priority.name}")
        print(f"  Risk Score: {risk_score}/10")
        print(f"  Concurrent Events: {concurrent_events}")
        print(f"  Risk Assessment: {self._generate_mock_assessment(event.priority)}")
        print()
    
    def _generate_mock_assessment(self, priority: EventPriority) -> str:
        """Generate mock risk assessment based on priority"""
        assessments = {
            EventPriority.LOW: "Normal activity, continue monitoring",
            EventPriority.MEDIUM: "Moderate risk, increased monitoring recommended",
            EventPriority.HIGH: "High risk detected, immediate analysis needed",
            EventPriority.CRITICAL: "CRITICAL: Potential depeg risk, emergency response required"
        }
        return assessments.get(priority, "Unknown risk level")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return {
            'total_events_processed': len(self.processed_events),
            'events_by_type': self.event_count.copy(),
            'last_processed': datetime.now().isoformat() if self.processed_events else None
        }
    
    def clear_history(self):
        """Clear event processing history"""
        self.processed_events.clear()
        for event_type in self.event_count:
            self.event_count[event_type] = 0

def setup_mock_agent():
    """Set up mock agent to handle events"""
    try:
        from core.event_bus import event_bus
        
        mock_agent = MockAIAgent()
        
        # Subscribe to all event types
        event_bus.subscribe(EventTypes.WHALE_ACTIVITY, mock_agent.handle_whale_activity)
        event_bus.subscribe(EventTypes.BALANCE_CHANGE, mock_agent.handle_balance_change)
        event_bus.subscribe(EventTypes.LARGE_TRANSACTION, mock_agent.handle_large_transaction)
        event_bus.subscribe(EventTypes.MULTI_FACTOR_RISK, mock_agent.handle_multi_factor_risk)
        
        print("Mock AI agent registered for all event types")
        return mock_agent
        
    except ImportError:
        print("Warning: Could not set up mock agent - event bus not available")
        return None