from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from dto import ResponseMessage


async def get_users(db: AsyncSession) -> Sequence[User]:
    sql_query = select(User).order_by(User.created_at.asc())
    result = await db.scalars(sql_query)

    users: Sequence[User] = result.all()

    return users


async def get_user(user_id: int, db: AsyncSession) -> User | None:
    # sql_query = select(User).where(User.id == user_id)
    # result = await db.scalars(sql_query)
    #
    # user: User | None = result.first()

    user: User | None = await db.get(User, user_id)
    return user


async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    sql_query = select(User).where(User.email == email)
    result = await db.scalars(sql_query)

    user: User | None = result.first()

    return user


async def create_user(user: User, db: AsyncSession) -> User:
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def delete_user(user: User, db: AsyncSession) -> ResponseMessage:
    await db.delete(user)
    await db.commit()

    return ResponseMessage(status_code=200, message=f"User {user.id} deleted")


async def update_user(user: User, db: AsyncSession) -> User:
    await db.commit()
    await db.refresh(user)

    return user
