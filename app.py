from fastapi import FastAPI
from api import router as ApiRouter
# from core.config import settings
# import uvicorn
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware

origins: list[str] = [settings.cors.origin]

app = FastAPI(
    title="api for notes"
)
app.include_router(router=ApiRouter, prefix="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def get_home():
    return "Home Page"

# if __name__ == "__app__":
#     uvicorn.run(
#         host=settings.run.host,
#         port=settings.run.port,
#         reload=True
#     )