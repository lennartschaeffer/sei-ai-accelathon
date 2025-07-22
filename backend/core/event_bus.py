import asyncio
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class EventPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Event:
    event_type: str
    data: Dict[str, Any]
    priority: EventPriority
    timestamp: float

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_queue = asyncio.PriorityQueue()
        self.running = False
        self.processor_task: Optional[asyncio.Task] = None
        self.event_counter = 0
    
    def subscribe(self, event_type: str, handler: Callable[[Event], None]):
        """Subscribe a handler to specific event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
        logger.info(f"Handler subscribed to {event_type}")
    
    async def publish(self, event: Event):
        """Publish an event to the bus"""
        self.event_counter += 1
        await self.event_queue.put((event.priority.value, self.event_counter, event))
        logger.debug(f"Published {event.event_type} event with {event.priority.name} priority")
    
    async def start_processing(self):
        """Start the event processing loop"""
        if self.running:
            return
        
        self.running = True
        self.processor_task = asyncio.create_task(self._process_events())
        logger.info("Event bus started processing")
    
    async def stop_processing(self):
        """Stop the event processing loop"""
        self.running = False
        if self.processor_task:
            self.processor_task.cancel()
            try:
                await self.processor_task
            except asyncio.CancelledError:
                pass
        logger.info("Event bus stopped processing")
    
    async def _process_events(self):
        """Internal event processing loop"""
        while self.running:
            try:
                _, _, event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                await self._handle_event(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing event: {e}")
    
    async def _handle_event(self, event: Event):
        """Handle a single event by calling all subscribers"""
        handlers = self.subscribers.get(event.event_type, [])
        
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Error in event handler: {e}")

# Global event bus instance
event_bus = EventBus()