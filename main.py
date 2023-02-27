from fastapi import FastAPI

app = FastAPI()

users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "user", "name": "Doe"},
    {"id": 3, "role": "postman", "name": "Sam"},
]

@app.get("/user/{users_id}")
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

users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "user", "name": "Doe"},
    {"id": 3, "role": "postman", "name": "Sam"},
]

@app.get("/user/{user_id}")
async def change_name(user_id: int, name: str):
    return