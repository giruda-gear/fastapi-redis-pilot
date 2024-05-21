from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.deliveries import deliveries
from routers.event import event

app = FastAPI()

app.include_router(deliveries)
app.include_router(event)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
