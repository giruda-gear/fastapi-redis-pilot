import json
import consumers

from fastapi import APIRouter, Depends, Request
from models.delivery import Devlivery
from models.event import Event
from redis_connection import get_redis

deliveries = APIRouter(prefix="/deliveries")


@deliveries.get("/{pk}/status")
async def get_state(pk: str, redis = Depends(get_redis)):
    state = redis.get(f"delivery:{pk}")

    if state is None:
        return {}

    return json.loads(state)


@deliveries.post("/create")
async def create(request: Request):
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
    ).save()

    state = consumers.handle_event({}, event)
    get_redis().set(f"delivery:{delivery.pk}", json.dumps(state))

    return state
