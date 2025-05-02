from fastapi import FastAPI
from .api import auth, player, game

app = FastAPI(title="Игра на выживание!")

app.include_router(auth.router)
app.include_router(player.router)
app.include_router(game.router)


@app.get("/")
async def root():
    return {"message": "Добро пожаловать в API многопользовательской игры"}
