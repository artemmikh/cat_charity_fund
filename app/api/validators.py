from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
from app.models import CharityProject
from app.schemas.charityproject import CharityProjectUpdate


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charityproject_crud.get_project_by_name(project_name,
                                                               session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Проект с таким именем уже существует!',
        )


async def check_charityproject_exists(
        charityproject_id: int, session: AsyncSession, ) -> CharityProject:
    charityproject = await charityproject_crud.get(charityproject_id, session)
    if charityproject is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charityproject


async def check_full_amount(
        full_amount: int,
        charityproject_id: int,
        session: AsyncSession,
) -> None:
    charityproject = await charityproject_crud.get(charityproject_id, session)
    if full_amount <= charityproject.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Требуемая сумма не может быть меньше уже внесённой!'
        )


async def check_close_project(
        project,
        session: AsyncSession,
):
    if project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя редактировать или удалять закрытый проект!'
        )
