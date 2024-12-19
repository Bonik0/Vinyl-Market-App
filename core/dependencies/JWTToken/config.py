from datetime import timedelta
from pydantic_settings import BaseSettings, SettingsConfigDict
from os.path import abspath, dirname, join


class JWTTokenSettings(BaseSettings):
    SECRET : str
    ALGORITHM : str
    ACCESS_TOKEN_TTL : timedelta
    REFRESH_TOKEN_TTL : timedelta
    model_config = SettingsConfigDict(
        extra = 'ignore',
        env_file = dirname(dirname(dirname(abspath(__file__)))) + '/env/jwttoken.env',
        frozen = True
    )


jwtsettings = JWTTokenSettings()

