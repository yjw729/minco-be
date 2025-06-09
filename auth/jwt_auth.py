from abc import ABC, abstractmethod
import time
import uuid
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

    def create_access_token(self, identity, user_claims: dict = None) -> str:
        """
        创建access_token
        """
        payload = {}

        payload["jti"] = str(uuid.uuid4())
        payload["sub"] = identity
        payload["iss"] = self.settings.issuer
        payload["aud"] = self.settings.audience
        payload["iat"] = datetime.now(timezone.utc)
        payload["exp"] = datetime.now(timezone.utc) + timedelta(
            seconds=self.settings.expires_delta
        )
        payload["user_claims"] = user_claims if user_claims else {}
        # TODO: 需要从数据库中获取
        payload["key"] = "5462877478"

        return jwt.encode(
            payload=payload, key=self.settings.key, algorithm=self.settings.algorithm
        )

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
            self.login_access_token = token
            self.login_payload = self.decode_token(token=token)

            # 没有key强制退出登录
            if "key" not in self.login_payload:
                return False

            return True
        except:
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


def create_jwt_auth_client() -> JWTAuth:
    """
    创建Jwt管理示例类
    """
    settings = JWTSettings(
        # 临时使用
        key="ve58mpGu0IKHbTkXJ2aXfImsH2V9ATh0",
        algorithm="HS256",
        issuer="http://localhost:8000",
        expires_delta=604800,
    )
    return JWTAuth(settings=settings)


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
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials:
            raise HTTPException(
                status_code=401, detail="Invalid authorization credentials."
            )

        if not credentials.scheme.lower() == "bearer":
            raise HTTPException(
                status_code=401, detail="Invalid authentication scheme."
            )

        if not await self.jwt_auth.init_login(credentials.credentials):
            raise HTTPException(
                status_code=401, detail="Invalid token or expired token."
            )

        if not await auth_service.get_login_user():
            raise HTTPException(
                status_code=401, detail="Invalid token or expired token."
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