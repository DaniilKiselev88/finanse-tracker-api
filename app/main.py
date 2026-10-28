from fastapi import FastAPI
from app.routes import users, transactions
app = FastAPI(title="Finance Tracker API")

app.include_router(users.router)
app.include_router(transactions.router)

@app.get("/")
def read_root():
    return {"message": "Привет, я запустил свой первый бэкенд"}