import json

from fastapi import HTTPException


def create_delivery(state, event):
    data = json.loads(event.data)

    return {
        "id": event.delivery_id,
        "budget": int(data["budget"]),
        "notes": data["notes"],
        "status": "ready",
    }


def start_delivery(state, event):
    if state["status"] != "ready":
        raise HTTPException(status_code=400, detail="delivery has already started")

    return state | {"status": "active"}


def pickup_products(state, event):
    data = json.loads(event.data)
    new_budget = state["budget"] - int(data["purchase_price"]) * int(data["quantity"])

    if new_budget < 0:
        raise HTTPException(status_code=400, detail="not enought budget")

    return state | {
        "budget": new_budget,
        "purchase_price": int(data["purchase_price"]),
        "quantity": int(data["quantity"]),
        "status": "collected",
    }


def deliver_products(state, event):
    data = json.loads(event.data)
    new_budget = state["budget"] + int(data["sell_price"]) * int(data["quantity"])
    new_quantity = state["quantity"] - int(data["quantity"])

    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="not enought quantity")

    return state | {
        "budget": new_budget,
        "sell_price": int(data["sell_price"]),
        "quantity": new_quantity,
        "status": "completed",
    }


def increase_budget(state, event):
    data = json.loads(event.data)
    state["budget"] += int(data["budget"])
    return state


def handle_event(state, event):
    match event.type:
        case "CREATE_DELIVERY":
            return create_delivery(state, event)
        case "START_DELIVERY":
            return start_delivery(state, event)
        case "PICKUP_PRODUCTS":
            return pickup_products(state, event)
        case "DELIVER_PRODUCTS":
            return deliver_products(state, event)
        case "INCREASE_BUDGET":
            return increase_budget(state, event)
        case _:
            raise ValueError(f"Unhandled event type: {event.type}")
