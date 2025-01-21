import uvicorn
from fastapi import FastAPI

from app.users.routes import users_router

app = FastAPI(title="Library API")

app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
