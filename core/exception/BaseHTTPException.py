from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from fastapi.responses import JSONResponse
from fastapi import Request
from enum import StrEnum, auto



class BaseHTTPErrorType(StrEnum):
    ERROR = auto()



class BaseHTTPExceptionModel(BaseModel):
    type : BaseHTTPErrorType = Field(description = 'Тип ошибки', default = BaseHTTPErrorType.ERROR)
    message : str = Field(description = 'Подробности')
    
    model_config = ConfigDict(frozen = True)
    



class BaseHTTPException(Exception):
    
    _all_responses_schemas : dict[type, dict[int, dict[str, Any]]] = {}
    
    def __init__(self, 
                status_code : int,
                ditail : BaseHTTPExceptionModel,
                headers : dict[str, str] | None = None,
                cookies : dict[str, str | dict[str, str]] | None = None,
                response_schema : dict[str, Any] | None = None
            ) -> None:
        if status_code > 599 or status_code < 300:
            raise ValueError('status_code have incorrect value')
        
        self.status_code = status_code
        self.headers = headers
        self.cookies = cookies if cookies is not None else {}
        self.ditail = {
                        'detail' : ditail.model_dump()
                    }
        self.__registrate_new_obj(status_code, ditail, response_schema)
    
    
    
    @classmethod    
    def get_responses_schemas(cls) -> dict[str, Any]:
        return cls._all_responses_schemas.get(cls)
    
    
    def __str__(self) -> str:
        return f'{self.status_code} : {self.ditail}'
    
    
    def __registrate_new_obj(self,
                            status_code : int,
                            ditail : BaseHTTPExceptionModel,
                            response_schema : dict[str, Any] | None = None
                        ) -> None:
        if response_schema is None:
            response_schema = {}
            
        response_schema['model'] = type(ditail)
        class_response_schema = self._all_responses_schemas[self.__class__]
        
        if class_response_schema.get(status_code) is None:
            class_response_schema[status_code] = {}
        
        class_response_schema[status_code].update(response_schema.copy())
            
            
    
    def __init_subclass__(cls) -> None:
        cls._all_responses_schemas[cls] = {}
        for base_cls in cls.__bases__:
            if cls._all_responses_schemas.get(base_cls) is not None:
                cls._all_responses_schemas[cls].update(cls._all_responses_schemas[base_cls].copy())
        




async def http_Exception_handler(request: Request, exc: BaseHTTPException) -> JSONResponse:
    
    response = JSONResponse(status_code = exc.status_code, content = exc.ditail, headers = exc.headers)
    
    for key, value in exc.cookies.items():
        if isinstance(value, str):
            response.set_cookie(key = key, value = value)
        else:
            response.set_cookie(key = key, **value)
        
    return response
            
            