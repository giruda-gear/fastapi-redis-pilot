import json
import consumers

from fastapi import APIRouter, Depends, Request
from models.delivery import Devlivery
from models.event import Event
from redis_connection import get_redis

deliveries = APIRouter(prefix="/deliveries")


@deliveries.get("/{pk}/status")
async def get_state(pk: str, redis=Depends(get_redis)):
    state = redis.get(f"delivery:{pk}")

    if state is None:
        state = build_state(pk)
        redis.set(f"delivery:{pk}", json.dumps(state))

    return json.loads(state)


@deliveries.post("/create")
async def create(request: Request, redis=Depends(get_redis)):
    body = await request.json()
    delivery = Devlivery(
        budget=body["data"]["budget"],
        notes=body["data"]["notes"],
    ).save()
    event = Event(
        delivery_id=delivery.pk,
        type=body["type"],
        data=json.dumps(
            body["data"],
        ),
    )
    state = consumers.handle_event({}, event)
    event.save()
    redis.set(f"delivery:{delivery.pk}", json.dumps(state))

    return state


def build_state(pk: str):
    pks = Event.all_pks()
    all_events = [Event.get(pk) for pk in pks]
    events = [event for event in all_events if event.deliver_id == pk]
    state = {}

    for event in events:
        state = consumers.handle_event(state, event)

    return state
