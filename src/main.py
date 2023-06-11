from fastapi import FastAPI

from src import match_parser


app = FastAPI()
app.include_router(match_parser.router)
