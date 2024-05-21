import json


def create_delivery(state, event):
    data = json.loads(event.data)

    return {
        "id": event.delivery_id,
        "budget": int(data["budget"]),
        "notes": data["notes"],
        "status": "ready",
    }


def start_delivery(state, event):
    return state | {"status": "active"}


def pickup_products(state, event):
    data = json.loads(event.data)
    new_budget = state["budget"] - int(data["purchase_price"])

    return {
        "id": event.delivery_id,
        "budget": int(data["budget"]),
        "notes": data["notes"],
        "status": "ready",
    }


def handle_event(state, event):
    match event.type:
        case "CREATE_DELIVERY":
            return create_delivery(state, event)
        case "START_DELIVERY":
            return start_delivery(state, event)
        case "PICKUP_PRODUCTS":
            return pickup_products(state, event)
        case _:
            raise ValueError(f"Unhandled event type: {event.type}")
