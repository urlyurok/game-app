from fastapi import FastAPI

app = FastAPI(title="Мультиплеерная игра KvadratLife")


@app.get("/")
async def root():
    return {"message": "Привет! Добро пожаловать"}
