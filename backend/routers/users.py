from collections.abc import Sequence
from fastapi import APIRouter, HTTPException, Depends, status
from schemas import UserCreate, UserResponse, UserUpdate
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from db import db_helper
from services import users as user_service
from errors import UserNotFoundError, UserAlreadyExistsError, RequiredFiledError

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(db_helper.get_db)) -> list[UserResponse]:
    users: Sequence[User] = await user_service.get_users(db)

    return [UserResponse.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(db_helper.get_db),
) -> UserResponse:
    try:
        user: User = await user_service.get_user(user_id, db)
        return UserResponse.model_validate(user)
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.post("/", response_model=UserResponse)
async def user_create(
    new_user: UserCreate, db: AsyncSession = Depends(db_helper.get_db)
) -> UserResponse:
    try:
        user: User = await user_service.create_user(new_user, db)
        return UserResponse.model_validate(user)
    except UserAlreadyExistsError as exc_existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc_existing)
        )
    except RequiredFiledError as exc_required_field:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc_required_field),
        )


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, new_user: UserUpdate, db: AsyncSession = Depends(db_helper.get_db)
) -> UserResponse:
    # TODO Убрать проверку на обязательные поля, для обновления все поля не обязательны!
    try:
        user: User = await user_service.get_user(user_id, db)
        updated_user = await user_service.update_user(new_user, user, db)
        return UserResponse.model_validate(updated_user)
    except RequiredFiledError as exc_required_field:
        print(f"------------------------------!!!!------------------------")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str("ОШИБКА!!!!!!!!!!!"),
        )
