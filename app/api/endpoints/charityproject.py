from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.base import SchemasBaseModel
from app.schemas.charityproject import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate)
from app.crud.charityproject import charityproject_crud
from app.api.validators import check_name_duplicate, check_charityproject_exists

router = APIRouter()


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True)
async def create_charity_project(
        project: CharityProjectCreate,
        # TODO насыпать прав суперюзеру
        # dependencies=[Depends(current_superuser)],
        session: AsyncSession = Depends(get_async_session)):
    await check_name_duplicate(project.name, session)
    new_room = await charityproject_crud.create(project, session)
    return new_room


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True)
async def get_charity_projects(
        session: AsyncSession = Depends(get_async_session)):
    all_projects = await charityproject_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    # TODO насыпать прав суперюзеру
    # dependencies=[Depends(current_superuser)],
)
async def partially_update_charityproject(
        charityproject_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session), ):
    project = await check_charityproject_exists(
        charityproject_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    # TODO требуемая сумма не меньше уже внесённой
    # TODO Никто не может менять через API размер внесённых средств
    # TODO Никто не может модифицировать закрытые проекты
    # TODO Никто не может изменять даты создания и закрытия проектов
    project = await charityproject_crud.update(
        project, obj_in, session)
    return project


@router.delete(
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    # TODO насыпать прав суперюзеру
    # dependencies=[Depends(current_superuser)],
)
async def remove_charityproject(
        charityproject_id: int,
        session: AsyncSession = Depends(get_async_session), ):
    project = await check_charityproject_exists(
        charityproject_id, session
    )
    # TODO Никто не может удалять закрытые проекты
    project = await charityproject_crud.remove(project, session)
    return project
