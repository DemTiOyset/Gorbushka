from fastapi import APIRouter, Request, HTTPException, Body
from starlette.responses import JSONResponse
from typing import Any

from api.enums import *
from api.message_schemas import *
from api.param_shemas import *


router = APIRouter(
    prefix="/webhook",
    tags=["webhook"]
)

@router.post("/notification")
async def notification(request: Request, payload: dict[str, Any] = Body(example={"example": "value"})):
    try:
        message = BaseDTO.model_validate(payload)

    except Exception:
        er = NotificationApiErrorDTO(
            message="Неверный тип уведомления.",
            type=NotificationApiErrorType.WRONG_EVENT_FORMAT,
            status_code=400
            )
        return JSONResponse(status_code=400, content=er.model_dump())


    return message



