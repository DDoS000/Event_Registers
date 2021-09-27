from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Add routers
# v1_router = APIRouter(prefix="/v1")
# v1_router.include_router(.........._router, tags=["......."])
# app.include_router(.....)

if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port = 8000, reload = True)
