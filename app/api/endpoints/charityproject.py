from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.charityproject import CharityProjectBase, CharityProjectDB

router = APIRouter()


@router.post('/', response_model=CharityProjectDB)
async def create_charity_project(
        project: CharityProjectBase, ):
    return project
