from typing import Type

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.exceptions import ObjectNotFoundException
from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.base import DataMapper
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPassword, User


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr) -> UserWithHashedPassword:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return UserWithHashedPassword.model_validate(model, from_attributes=True)
