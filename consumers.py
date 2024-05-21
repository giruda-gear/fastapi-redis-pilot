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
        "budget": new_budget,
        "purchase_price": int(data["purchase_price"]),
        "quantity": int(data["quantity"]),
        "status": "collected",
    }


def deliver_products(state, event):
    data = json.loads(event.data)
    new_budget = state["budget"] + int(data["sell_price"]) * int(data["quantity"])
    new_quantity = state["quantity"] - int(data["quantity"])

    return {
        "budget": new_budget,
        "sell_price": int(data["sell_price"]),
        "quantity": new_quantity,
        "status": "completed",
    }


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
        case _:
            raise ValueError(f"Unhandled event type: {event.type}")
