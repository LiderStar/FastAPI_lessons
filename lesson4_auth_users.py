from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Depends
from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import BaseModel, Field
from pydantic.config import Enum

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

app = FastAPI()

users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "user", "name": "Doe"},
    {"id": 3, "role": "postman", "name": "Sam"},
    {"id": 4, "role": "investor", "name": "Homer", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
    ]},
]



class Type_degree(Enum):
    newbie = 'newbie'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: Type_degree


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]]


@app.get("/user/{users_id}", response_model=List[User])
async def get_id(user_id: int):
    return [user for user in users if user.get("id") == user_id]


trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
    {"id": 3, "user_id": 1, "currency": "BTC", "side": "sell", "price": 127, "amount": 2.15},
    {"id": 4, "user_id": 1, "currency": "BTC", "side": "sell", "price": 129, "amount": 2.17},
]


@app.get("/traders")
async def get_trade(limit: int, offset: int):
    return trades[offset:][:limit]


users2 = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "user", "name": "Doe"},
    {"id": 3, "role": "postman", "name": "Sam"},
]


@app.post("/user/{user_id}")
async def change_name(user_id: int, name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, users2))[0]
    current_user['name'] = name
    return {"status": 200, "data": current_user}


trades_cri = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
    {"id": 3, "user_id": 1, "currency": "BTC", "side": "sell", "price": 127, "amount": 2.15},
    {"id": 4, "user_id": 1, "currency": "BTC", "side": "sell", "price": 129, "amount": 2.17},
]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post("/trades")
async def add_trades(trades: List[Trade]):
    trades_cri.extend(trades)
    return {"status": 200, "data": trades_cri}


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
    )

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def protected_route():
    return f"Hello anonymus"