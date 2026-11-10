from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from reposytories import users as crud_users
from errors import UserNotFoundError, UserAlreadyExistsError, RequiredFiledError
from schemas import UserCreate


async def get_users(db: AsyncSession) -> Sequence[User]:
    users: Sequence[User] = await crud_users.get_users(db)

    return users


async def get_user(user_id: int, db: AsyncSession) -> User:
    user: User | None = await crud_users.get_user(user_id, db)

    if user is None:
        raise UserNotFoundError(user_id)

    return user


async def create_user(new_user: UserCreate, db: AsyncSession) -> User:

    await _check_required_fields(new_user)
    await _check_email(new_user, db)

    user: User = User(
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        password_hash=new_user.password_hash,
    )

    result: User = await crud_users.create_user(user, db)

    return result


async def _check_required_fields(new_user: UserCreate) -> bool:
    if new_user.email is None:
        raise RequiredFiledError("email")

    if new_user.password_hash is None:
        raise RequiredFiledError("password")

    return True


async def _check_email(new_user: UserCreate, db: AsyncSession) -> bool:
    user: User | None = await crud_users.get_user_by_email(new_user.email, db)

    if user is not None:
        raise UserAlreadyExistsError(new_user.email)

    return True
