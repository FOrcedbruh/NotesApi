from fastapi import FastAPI
from api import router as ApiRouter

app = FastAPI(
    title="api for notes"
)
app.include_router(router=ApiRouter, prefix="/api/v1")



@app.get("/")
def get_home():
    return "Home Page"

