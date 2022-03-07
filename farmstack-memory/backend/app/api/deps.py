from fastapi import Depends

from schemas.token import TokenPayload
from core.security import validate_token


def get_current_user_id(
    payload=Depends(validate_token)
):
    token_payload = TokenPayload(**payload)
    user_id = token_payload.dict().get('sub')
    return user_id
