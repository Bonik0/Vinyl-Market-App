from pydantic import Field, ConfigDict, AliasChoices
from uuid import UUID, uuid4
from core.schemas.BaseModel import BaseModel
from .config import jwtsettings
from core.schemas.user import NonPrivateUserInfoOut
from datetime import datetime, timezone



def access_token_timestamp() -> int:
    return int((datetime.now(timezone.utc).astimezone().timestamp() + jwtsettings.ACCESS_TOKEN_TTL.total_seconds()) * 1000)


class IssuedJWTTokenData(BaseModel):
    
    jti : UUID = Field(description = 'UUID токена', default_factory = uuid4)
    device_id : UUID = Field(description = 'Индификатор устройства')
    
    model_config = ConfigDict(title = 'Информация о токене')
    
    
class IssuedJWTTokenPayloadOut(IssuedJWTTokenData, NonPrivateUserInfoOut):
    pass
    
    
    
class IssuedJWTTokensOut(BaseModel):
    
    access_token : str = Field(description = 'access_token')
    refresh_token : str = Field(description = 'refresh_token')
    exp : float = Field(default_factory = access_token_timestamp, description = 'Время жизни access_token')
    
    model_config = ConfigDict(title = 'Сгенерированые access_token и refresh_token')
    
    
    
class IssuedJWTTokensWithDataOut(BaseModel):
    
    tokens : IssuedJWTTokensOut
    data : tuple[IssuedJWTTokenData, IssuedJWTTokenData] 
    
    
    

    