from fastapi import HTTPException, Request
from fastapi_injector import Injected
from api.user.models import User, UserCreate
from api.user.service import UserService
from api.user.repository import UserRepository
from init_data_py import InitData
from config import Config


def get_current_user(
    request: Request,
    user_service: UserService = Injected(UserService),
    config: Config = Injected(Config),
) -> User:

    return get_current_user_mock(request=request, user_service=user_service)
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = auth_header.split(" ")[-1]

    init_data = InitData.parse(token)
    if not init_data.validate(bot_token=config.bot_token):
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = user_service.get_user_by_telegram_id(init_data.user.id)

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user


def get_current_user_mock(
    request: Request,
    user_service: UserService = Injected(UserService),
) -> User:
    # Test user details
    test_user_1_telegram_id = 123456789
    test_user_2_telegram_id = 987654321
    
    # Access repository through service
    user_repository = user_service.user_repository
    
    # Check if test users exist and create them if needed
    user_1_exists = user_repository.user_by_telegram_id_exists(test_user_1_telegram_id)
    user_2_exists = user_repository.user_by_telegram_id_exists(test_user_2_telegram_id)
    
    # Create test user 1 if it doesn't exist
    if not user_1_exists:
        user_1_create = UserCreate(
            telegram_user_id=test_user_1_telegram_id,
            username="test_user_1",
            first_name="Test",
            last_name="User One",
            photo_url=None
        )
        user_repository.save(User(**user_1_create.model_dump()))
    
    # Create test user 2 if it doesn't exist
    if not user_2_exists:
        user_2_create = UserCreate(
            telegram_user_id=test_user_2_telegram_id,
            username="test_user_2",
            first_name="Test",
            last_name="User Two",
            photo_url=None
        )
        user_repository.save(User(**user_2_create.model_dump()))
    
    # Always return the first test user
    user_1 = user_repository.find_user_by_telegram_id(test_user_1_telegram_id)
    
    # This should never be None since we just created it, but handle it just in case
    if user_1 is None:
        # Fallback: recreate the user if somehow it doesn't exist
        user_1_create = UserCreate(
            telegram_user_id=test_user_1_telegram_id,
            username="test_user_1",
            first_name="Test",
            last_name="User One",
            photo_url=None
        )
        user_1 = user_repository.save(User(**user_1_create.model_dump()))
    
    return user_1
