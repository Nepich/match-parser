from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import match_parser


app = FastAPI()
app.include_router(match_parser.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
