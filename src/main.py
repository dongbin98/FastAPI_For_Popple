import uvicorn
from fastapi import FastAPI

from src.domain.user import user_router

# FastAPI 객체 생성
app = FastAPI()

app.include_router(user_router.router)


# Route Base Path
@app.get("/")
def index():
    return {"Popple": "Root Dir"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
