from typing import Literal

from fastapi import APIRouter, status


router = APIRouter()


RESPONSE_MODEL = Literal["OK"]


@router.get("/", response_model=RESPONSE_MODEL, status_code=status.HTTP_200_OK)
def healthcheck() -> RESPONSE_MODEL:
    return "OK"
