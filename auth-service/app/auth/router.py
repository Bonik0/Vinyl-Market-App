from fastapi import APIRouter, Depends, Request
from .schemas import UserRegistrationCredentialsIn, UserLoginCredentialsIn, RefreshTokenIn
from .dao import AuthDAO
from .errors import AuthException
from core.dependencies.JWTToken import IssuedJWTTokensOut, JWTException, TokenValidation
from core.models.postgres import UserRole
from core.schemas import SellerInfoIn
from aiohttp import ClientSession
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse



router = APIRouter(tags = ['Аунтификация'],
                   responses = AuthException.get_responses_schemas()
                )



@router.post(path = '/registration', summary = 'Регистация пользователя')
async def registrate(user_credentials : UserRegistrationCredentialsIn) -> IssuedJWTTokensOut:
    return await AuthDAO.registrate(user_credentials)



@router.post(path = '/login', summary = 'Вход в аккаунт')
async def login(user_credentials : UserLoginCredentialsIn) -> IssuedJWTTokensOut:
    return await AuthDAO.login(user_credentials)



@router.post(path = '/seller-registration',
            summary = 'Регистация продавца',
            dependencies = [Depends(TokenValidation.check_access_token)],
            responses = JWTException.get_responses_schemas()
        )
async def seller_registration(request : Request, seller_credentials : SellerInfoIn) -> IssuedJWTTokensOut:
    return await AuthDAO.seller_registrate(request.state.user, seller_credentials)


@router.post(path = '/update-tokens', summary = 'Обновление токенов', responses = JWTException.get_responses_schemas())
async def update_tokens(request : Request, user_credentials : RefreshTokenIn) -> IssuedJWTTokensOut:
    return await AuthDAO.update_tokens(user_credentials)


