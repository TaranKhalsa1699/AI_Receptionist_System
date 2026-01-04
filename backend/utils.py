import httpx
import logging
from config import WEBHOOK_URL
from models import WebhookPayload

async def trigger_webhook(payload: WebhookPayload) -> bool:
    """
    Triggers the external webhook with patient data.
    Returns True if successful (200 OK), False otherwise.
    Swallows exceptions to prevent crashing the flow.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.post(
                WEBHOOK_URL,
                json=payload.dict(),
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return True
    except httpx.HTTPStatusError as e:
        logging.error(f"Webhook Failed (Status {e.response.status_code}): {e.response.text}")
        return False
    except Exception as e:
        logging.error(f"Webhook Trigger Error: {e}")
        return False
