"""main application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from loguru import logger

import uvicorn

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("application:app", host="0.0.0.0", port=80, reload=True)