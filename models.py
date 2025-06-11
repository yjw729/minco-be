from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    """API统一响应格式"""
    code: int = 0
    message: str = "success"
    data: Optional[T] = None

class LoginRequestDto(BaseModel):
    """登录请求"""
    username: str
    password: str

class AuthResponseDto(BaseModel):
    """认证响应"""
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str

class FileUploadResponse(BaseModel):
    """文件上传响应"""
    endpoint: Optional[str] = None
    endpoints: Optional[List[str]] = None

class TestConnectRequestDto(BaseModel):
    """测试连接请求"""
    uuid: Optional[str] = None

class TestConnectResponseDto(BaseModel):
    """测试连接响应"""
    status: str
    message: str
    uuid: Optional[str] = None
