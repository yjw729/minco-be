from datetime import datetime, timedelta
from typing import Optional
import jwt
from models import AuthResponseDto
from util.logging import logger
from mysql_client import get_db_session, UserModel

class AuthService:
    # 配置
    # 临时
    SECRET_KEY = "ve58mpGu0IKHbTkXJ2aXfImsH2V9ATh0"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """创建访问令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def login(self, username: str, password: str) -> AuthResponseDto:
        """用户登录"""
        with get_db_session() as db:
            user = db.query(UserModel).filter(UserModel.username == username).first()
            if not user:
                raise Exception("用户不存在")
            
            if user.password != password:  # 实际应用中应该使用加密密码
                raise Exception("密码错误")
            
            if user.status != 1:
                raise Exception("用户已被禁用")
            
            access_token = self.create_access_token(
                data={"sub": str(user.id)},
                expires_delta=timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            
            return AuthResponseDto(
                access_token=access_token,
                token_type="bearer",
                user_id=user.id,
                username=user.username
            )

    async def get_login_user(self):
        """获取当前登录用户"""
        from auth.jwt_auth import get_jwt_auth_client
        jwt_auth = get_jwt_auth_client()
        payload = jwt_auth.get_login_payload()
        
        if not payload:
            raise Exception("未登录")
        
        user_id = payload.get("sub")
        if not user_id:
            raise Exception("无效的token")
        
        with get_db_session() as db:
            user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()
            if not user:
                raise Exception("用户不存在")
            
            if user.status != 1:
                raise Exception("用户已被禁用")
            
            return user
