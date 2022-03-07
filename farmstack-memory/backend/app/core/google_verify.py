import requests
import cachecontrol

from google.oauth2 import id_token
from google.auth.transport.requests import Request

from core.config import settings

proxies = {
    'https': 'http://127.0.0.1:7890'
}

session = requests.Session()
session.proxies.update(proxies)
# keep session for google only update credentials per day
cached_session = cachecontrol.CacheControl(session)


request = Request(session=session)

client_id = settings.CLIENT_ID


def validate_google_token(token_id):
    id_info = id_token.verify_oauth2_token(token_id, request, client_id)
    payload = id_info
    return payload
