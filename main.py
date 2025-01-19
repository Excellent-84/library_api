import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Library API")


@app.get("/")
def root():
    return {"message": "Welcome to the Library API!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
