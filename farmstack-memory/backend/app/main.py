from urllib.parse import urlencode

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.datastructures import QueryParams

from api.v1.api import api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.middleware('http')
async def drop_blank_query_params_middleware(request: Request, call_next):
    _scope = request.scope
    if request.method != 'GET':
        return await call_next(request)
    if not _scope or not _scope.get('query_string'):
        return await call_next(request)

    def _process_query_params(query_params):
        _query_params = QueryParams(query_params)
        return urlencode([
            # using `_query_params.items()` will mistakenly process list parameters
            (k, v) for k, v in _query_params._list if v and v.strip()  # noqa
        ])

    # for POST operation, it should be encode to bytes
    _scope['query_string'] = _process_query_params(_scope['query_string']).encode('utf-8')
    return await call_next(Request(_scope, request.receive, request._send))  # noqa


app.include_router(api_router)
