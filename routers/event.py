import json
import consumers
from fastapi import APIRouter, Depends, Request
from models.event import Event
from redis_connection import get_redis
from routers.deliveries import get_state


event = APIRouter(prefix="/event")


@event.post("/")
async def dispatch(request: Request, redis=Depends(get_redis)):
    body = await request.json()
    delivery_id = body["delivery_id"]
    event = Event(
        delivery_id=delivery_id,
        type=body["type"],
        data=json.dumps(
            body["data"],
        ),
    )

    state = await get_state(delivery_id, redis)
    new_state = consumers.handle_event(state, event)
    event.save()
    redis.set(f"delivery:{delivery_id}", json.dumps(new_state))

    return new_state
