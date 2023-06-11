from fastapi import APIRouter

from . import services, handlers  # , repos

# repo = repos.ParserRepoV1()
service = services.ParserServiceV1()
handler = handlers.ParserHandlerV1(service)

router = APIRouter(
    prefix='/get_matches',
    tags=['get_matches'],
)

router.add_api_route('/', handler.get_matches, methods=['post'])
