import asyncio

from fastapi import FastAPI

from src import match_parser
# from src.match_parser import handler


app = FastAPI()
app.include_router(match_parser.router)

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     pattern = 'Энциклопедией называют также научное справочное пособие, '
#     url = 'https://ru.wikipedia.org/wiki/%D0%AD%D0%BD%D1%86%D0%B8%D0%BA%D0%BB%D0%BE%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F'
#
#     async def main():
#         task = asyncio.create_task(handler.get_matches(url, pattern))
#         result = await task
#         print(result)
#
#     loop.run_until_complete(main())
