from typing import Optional

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charityproject import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_room_id = db_project_id.scalars().first()
        return db_room_id

    async def get_newest_open_project(
            self, session: AsyncSession, ) -> Optional[CharityProject]:
        newest_open_project = await session.execute(
            select(CharityProject).filter(
                CharityProject.fully_invested == False)
            .order_by(desc(CharityProject.create_date))
            .limit(1))
        return newest_open_project.scalars().first()


charityproject_crud = CRUDCharityProject(CharityProject)
