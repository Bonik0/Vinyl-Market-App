from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from core.schemas import PrivateUserInfoOut
from .dao import UserAccountDAO
from core.services_and_endpoints import endpoints

templates = Jinja2Templates(directory = './app/templates')



router = APIRouter(
                   tags = ['Пользовательский аккаунт'],
                )



@router.get(path = '/account', summary = 'Информация о пользователе')
async def user_account(request : Request) -> PrivateUserInfoOut:
    return await UserAccountDAO.get_user_by_user_id(user_id = request.state.user.user_id)    
    
    
@router.get(path = '/logout', summary = 'Выход из аккаунта')
async def logout(request : Request) -> str:
    await UserAccountDAO.logout(request.state.user.device_id)
    return endpoints.LOGIN_ENDPOINT



@router.get(path = '/full-logout', summary = 'Выход из аккаунта со всех устройств')
async def full_logout(request : Request) -> str:
    await UserAccountDAO.full_logout(request.state.user.user_id)
    return endpoints.LOGIN_ENDPOINT
