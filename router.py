from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uuid
from models import ApiResponse, AuthResponseDto, LoginRequestDto, TestConnectRequestDto, TestConnectResponseDto
from service import auth_service
from auth.jwt_auth import JWTAuthBearer
from util.logging import logger

router = APIRouter()
auth_router = APIRouter(dependencies=[Depends(JWTAuthBearer())])

def api_response(data=[], code=0, message="success", status_code=200):
    """API返回结果包装函数"""
    content = ApiResponse(code=code, message=message, data=data)
    return JSONResponse(content=jsonable_encoder(content), status_code=status_code)

def build_auth_response(auth_response: AuthResponseDto):
    """构建认证响应"""
    response = api_response(data=auth_response)
    access_token = auth_response.access_token
    response.set_cookie(
        key="auth_token",
        value=access_token,
        domain=".example.com",
        max_age=604800
    )
    return response

# 认证相关路由
@router.post(
    "/auth/login",
    name="登录接口",
    response_model=ApiResponse[AuthResponseDto],
)
async def user_login(data: LoginRequestDto):
    """用户登录"""
    return build_auth_response(
        await auth_service.login(username=data.username, password=data.password)
    )

@auth_router.post(
    "/auth/logout",
    name="登出接口",
    response_model=ApiResponse
)
async def user_logout():
    """用户登出"""
    user = await auth_service.get_login_user()
    logger.info(f"user logout, user: {user.id}")
    return api_response(data=[])

# 测试相关路由
@router.post(
    "/test/connect_test",
    name="测试连接接口",
    response_model=ApiResponse[TestConnectResponseDto],
)
async def test_connect(data: TestConnectRequestDto):
    """测试连接"""
    response_data = TestConnectResponseDto(
        status="success",
        message="Connection successful",
        uuid=data.uuid
    )
    return api_response(data=response_data)
