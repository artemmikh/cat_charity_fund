from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
from app.schemas.charityproject import CharityProjectDB
from app.schemas.donation import DonationDB


async def investing_new_donation(
        donation: DonationDB,
        session: AsyncSession,
):
    project = await charityproject_crud.get_oldest_open_project(session)
    if project is None:
        return donation

    remaining_donation_amount = donation.full_amount
    invested_amount = 0

    while remaining_donation_amount > 0:
        project = await charityproject_crud.get_oldest_open_project(session)
        if project is None:
            break

        need_donation = project.full_amount - project.invested_amount
        if need_donation <= remaining_donation_amount:
            project.invested_amount += need_donation
            invested_amount += need_donation
            remaining_donation_amount -= need_donation
        else:
            project.invested_amount += remaining_donation_amount
            invested_amount += remaining_donation_amount
            remaining_donation_amount = 0

        if project.invested_amount >= project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.now()

    donation.invested_amount = invested_amount
    if remaining_donation_amount == 0:
        donation.close_date = datetime.now()
        donation.fully_invested = True
    await session.commit()
    return donation


async def investing_to_new_project(
        project: CharityProjectDB,
        session: AsyncSession, ):
    need_donation = project.full_amount

    if need_donation <= 0:
        await session.commit()
        return project

    while True:
        donation = await charityproject_crud.get_oldest_open_donation(session)
        if donation is None:
            break

        free_donation = donation.full_amount - donation.invested_amount

        if free_donation < need_donation:
            project.invested_amount += free_donation
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            donation.close_date = datetime.now()
            need_donation -= free_donation

        elif free_donation == need_donation:
            project.invested_amount = project.full_amount
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            donation.close_date = datetime.now()
            project.fully_invested = True
            project.close_date = datetime.now()
            break

        elif free_donation > need_donation:
            project.invested_amount = project.full_amount
            donation.invested_amount += need_donation
            project.fully_invested = True
            project.close_date = datetime.now()
            break

    await session.commit()
    return project
