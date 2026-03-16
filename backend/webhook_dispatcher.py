"""
Webhook Dispatcher for D2C Voice-First Agent.

Sends HTTP POST requests to a brand's registered `webhook_url` when
important events occur, such as ticket creation or ticket resolution.
"""

import httpx
import asyncio
from typing import Any, Dict
from logger import get_logger

log = get_logger()

# Background event queue for webhooks
_webhook_queue: asyncio.Queue = asyncio.Queue()


async def _webhook_worker():
    """Background worker to process webhook dispatches."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        while True:
            try:
                url, payload = await _webhook_queue.get()
                log.info(f"Dispatching webhook event '{payload.get('event')}' to {url}")
                
                response = await client.post(url, json=payload)
                response.raise_for_status()
                log.info(f"Webhook delivered successfully: {url} (status={response.status_code})")
            except Exception as e:
                log.error(f"Failed to deliver webhook to {url}: {e}")
            finally:
                _webhook_queue.task_done()


def start_webhook_worker():
    """Start the background webhook worker task."""
    asyncio.create_task(_webhook_worker())


def dispatch_event(webhook_url: str, event_type: str, data: Dict[str, Any]):
    """
    Queue an event to be dispatched to a brand's webhook URL.
    
    event_type: "ticket.created", "ticket.closed", etc.
    """
    if not webhook_url:
        return
        
    payload = {
        "event": event_type,
        "data": data,
    }
    
    # Put in background queue so it doesn't block request threads.
    # We use a slight hack to run this safely from sync contexts if needed,
    # but primarily this should be called correctly within the async web server.
    try:
        loop = asyncio.get_running_loop()
        loop.call_soon_threadsafe(_webhook_queue.put_nowait, (webhook_url, payload))
    except RuntimeError:
        # If no running loop, we can't easily dispatch. 
        # In this app, it's mostly run under FastAPI anyway.
        log.warning(f"Failed to queue webhook '{event_type}' - no running event loop")
