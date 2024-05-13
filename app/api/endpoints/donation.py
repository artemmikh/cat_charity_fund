from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.base import SchemasBaseModel
from app.schemas.donation import (
    DonationDB,
    DonationUpdate,
    DonationCreate,
    DonationDBSuperuser)
from app.crud.donation import donation_crud
from app.core.user import current_user
from app.models import User

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)):
    new_donation = await donation_crud.create(donation, session, user)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={'user_id'}
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    donations = await donation_crud.get_by_user(user=user, session=session)
    return donations


@router.get('/',
            response_model=list[DonationDBSuperuser],
            dependencies=[Depends(current_superuser)], )
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)):
    all_donations = await donation_crud.get_multi(session)
    return all_donations
