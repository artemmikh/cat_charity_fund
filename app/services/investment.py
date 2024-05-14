from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.donation import DonationDB, DonationCreate
from app.crud.charityproject import charityproject_crud


async def investing(
        donation: DonationDB,
        session: AsyncSession,
):
    print('1')
    project = await charityproject_crud.get_newest_open_project(session)
    if project is None:
        return donation
    print('2')

    remaining_donation_amount = donation.full_amount
    while remaining_donation_amount > 0:
        project = await charityproject_crud.get_newest_open_project(session)
        if project is None:
            break

        need_donation = project.full_amount - project.invested_amount
        if need_donation <= remaining_donation_amount:
            project.invested_amount += need_donation
            remaining_donation_amount -= need_donation
        else:
            project.invested_amount += remaining_donation_amount
            remaining_donation_amount = 0

        if project.invested_amount >= project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.now()

        await session.commit()
        await session.refresh(project)

    donation.invested_amount = donation.full_amount - remaining_donation_amount
    return donation
