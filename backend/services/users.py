from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from reposytories import users as crud_users
from errors import UserNotFoundError, UserAlreadyExistsError, RequiredFiledError
from schemas import UserCreate, UserUpdate


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


async def update_user(new_user: UserUpdate, user: User, db: AsyncSession) -> User:
    """
    Если поле не передано, тогда выбросим его 'exclude_unset=True',
    но если передано и даже None, тогда примем, т.к. возможно пользователь захочет очистить поле.
    Но пользователь не может очистить обязательные поля.

    Т.е. Логика следующая, допустим:
        1. если поле передано и 'first_name=None' тогда подставим текущее имя пользователя
        2. если поле передано и в нем имя отличается от текущего имени пользователя, тогда заменяем
        3. если поле вообще не передано, просто выбрасываем из запроса
    """
    data = new_user.model_dump(
        exclude_unset=True
    )  # Не переданные поля выбрасываем из словаря
    print(
        f"new_user==update_user=== {data}"
    )  # {'first_name': 'John', 'last_name': 'Doe'}

    print(f"user ====1====== {user}")
    # Если ключ "last_name" есть в словаре data например "{'first_name': 'John', 'last_name': 'Doe'}"
    # Если ключа "last_name" нет в словаре, тогда pydantic подставит None по умолчанию и null запишется в базу
    if "last_name" in data:
        setattr(user, "last_name", new_user.last_name)  # Тогда подставим значение

    # Если ключ "first_name" есть в словаре и значение не None тогда запишем его в базу
    # Если ключа нет в словале, pydantic подставит None, но None не пропустим для записи
    # TODO Сделать проверку на пустые строки, в такой реализации
    #  пройдет запрос с first_name="" т.к. пустая строка не является None - Решено!
    if (
        "first_name" in data
        and new_user.first_name is not None
        and new_user.first_name.strip() != ""
    ):
        setattr(user, "first_name", new_user.first_name.strip())

    # Аналогично с "first_name", пустое не пропустим для записи
    # TODO Проверить наличие такого email у других пользователей,
    #  чтобы под зарегистрированным email не могли зарегистрироваться повторно
    if "email" in data and new_user.email is not None and new_user.email.strip() != "":
        setattr(user, "email", new_user.email.strip())

    # Аналогично с "first_name", пустое не пропустим для записи
    if (
        "password_hash" in data
        and new_user.password_hash is not None
        and new_user.password_hash.strip() != ""
    ):
        setattr(user, "password_hash", new_user.password_hash.strip())

    print(f"user =====2===== {user}")

    result: User = await crud_users.update_user(user, db)
    return result


async def _check_required_fields(new_user: UserCreate) -> bool:
    required_fields = ("email", "password_hash", "first_name")
    for name, value in new_user:
        if name in required_fields and value is None:
            raise RequiredFiledError(name)

    # if new_user.email is None:
    #     print(f"==========email============_check_required_fields===========")
    #     raise RequiredFiledError("email")
    #
    # if new_user.password_hash is None:
    #     print(f"==========password_hash============_check_required_fields==========")
    #     raise RequiredFiledError("password")
    #
    # if new_user.first_name is None:
    #     print(f"==========first_name============_check_required_fields==========")
    #     raise RequiredFiledError("first_name")
    return True


async def _check_email(new_user: UserCreate, db: AsyncSession) -> bool:
    user: User | None = await crud_users.get_user_by_email(new_user.email, db)

    if user is not None:
        raise UserAlreadyExistsError(new_user.email)

    return True
