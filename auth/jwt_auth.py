from abc import ABC, abstractmethod
import time
import uuid
import json
from fastapi import Request, HTTPException, Depends, status
from fastapi.security.http import HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field

from service import auth_service

class JWTSettings(BaseModel):

    key: str
    algorithm: str
    issuer: str = Field(default=None)
    audience: str = Field(default=None)
    expires_delta: int = Field(default=7200)


class JWTAuth:

    def __init__(self, settings: JWTSettings) -> None:
        self.settings = settings
        self.login_access_token = None
        self.login_payload = {}



    def decode_token(self, token: str) -> dict:
        """
        解析access_token
        """
        return jwt.decode(
            jwt=token,
            issuer=self.settings.issuer,
            audience=self.settings.audience,
            key=self.settings.key,
            algorithms=self.settings.algorithm,
        )

    async def init_login(self, token: str):
        """
        设置当前认证token信息
        """
        try:
            from util.logging import logger
            
            logger.debug(f"🔍 开始验证JWT Token: {token[:50]}...")
            
            self.login_access_token = token
            self.login_payload = self.decode_token(token=token)
            
            logger.debug(f"🔍 Token解码成功，payload: {json.dumps({k: v for k, v in self.login_payload.items() if k not in ['key']}, ensure_ascii=False)}")

            # 没有key强制退出登录
            if "key" not in self.login_payload:
                logger.warning(f"❌ JWT认证失败: Token缺少必需的key字段")
                return False

            logger.info(f"✅ JWT认证成功，用户ID: {self.login_payload.get('sub')}")
            return True
        except jwt.ExpiredSignatureError:
            logger.warning(f"❌ JWT认证失败: Token已过期")
            return False
        except jwt.InvalidIssuerError:
            logger.warning(f"❌ JWT认证失败: Token发行者无效")
            return False
        except jwt.InvalidSignatureError:
            logger.warning(f"❌ JWT认证失败: Token签名无效")
            return False
        except jwt.InvalidTokenError as e:
            logger.warning(f"❌ JWT认证失败: Token无效 - {str(e)}")
            return False
        except Exception as e:
            logger.error(f"❌ JWT认证失败: 未知错误 - {str(e)}")
            return False

    def get_login_payload(self) -> dict:
        """
        获取登录负载信息
        """
        return self.login_payload

    async def logout(self):
        """
        退出登录
        """
        jti = self.login_payload.get("jti")

        if not jti:
            return


jwt_auth_client: JWTAuth = None


def get_jwt_auth_client():
    """
    获取jwt_auth client实例
    """
    global jwt_auth_client

    if jwt_auth_client:
        return jwt_auth_client

    settings = JWTSettings(
        key="ve58mpGu0IKHbTkXJ2aXfImsH2V9ATh0",
        algorithm="HS256",
        issuer="http://localhost:8000",
        expires_delta=604800,
    )
    jwt_auth_client = JWTAuth(settings=settings)

    return jwt_auth_client


class JWTAuthBearer(HTTPBearer):

    def __init__(self) -> None:
        super().__init__(auto_error=False)
        self.jwt_auth = get_jwt_auth_client()

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        """
        校验Token
        """
        from util.logging import logger
        
        # 记录认证开始
        client_ip = request.client.host if request.client else "unknown"
        endpoint = str(request.url.path)
        logger.debug(f"🔐 开始JWT认证 - 客户端: {client_ip}, 接口: {endpoint}")
        
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials:
            logger.warning(f"❌ JWT认证失败: 缺少Authorization头 - 客户端: {client_ip}, 接口: {endpoint}")
            raise HTTPException(
                status_code=401, detail="缺少认证凭据"
            )

        if not credentials.scheme.lower() == "bearer":
            logger.warning(f"❌ JWT认证失败: 认证方案无效 ({credentials.scheme}) - 客户端: {client_ip}, 接口: {endpoint}")
            raise HTTPException(
                status_code=401, detail="无效的认证方案，需要Bearer Token"
            )

        # 验证JWT Token
        token_valid = await self.jwt_auth.init_login(credentials.credentials)
        if not token_valid:
            logger.warning(f"❌ JWT认证失败: Token验证失败 - 客户端: {client_ip}, 接口: {endpoint}")
            raise HTTPException(
                status_code=401, detail="无效或过期的Token"
            )

        # 验证用户是否存在
        try:
            user = await auth_service.get_login_user()
            if not user:
                logger.warning(f"❌ JWT认证失败: 用户不存在 - 客户端: {client_ip}, 接口: {endpoint}")
                raise HTTPException(
                    status_code=401, detail="用户不存在或已被禁用"
                )
            logger.debug(f"✅ JWT认证成功 - 用户ID: {user.id}, 用户名: {user.username}, 客户端: {client_ip}, 接口: {endpoint}")
        except Exception as e:
            logger.warning(f"❌ JWT认证失败: 用户验证错误 - {str(e)} - 客户端: {client_ip}, 接口: {endpoint}")
            raise HTTPException(
                status_code=401, detail="用户验证失败"
            )

        return credentials


class JWTAdminAuthBearer(JWTAuthBearer):

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        """
        校验admin token
        """
        credetials = await super().__call__(request)

        payload = self.jwt_auth.get_login_payload()
        if int(payload.get("sub")) not in [1]:
            raise HTTPException(status_code=403, detail="Permission denied.")

        return credetials