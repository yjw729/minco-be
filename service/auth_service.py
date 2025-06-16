from datetime import datetime, timedelta, timezone
from typing import Optional, List
import jwt
import json
import uuid
from models import AuthResponseDto, RegisterResponseDto, UserDto
from util.logging import logger, api_logger
from mysql_client import get_db_session, UserModel

class AuthService:
    # 配置
    # 临时
    SECRET_KEY = "ve58mpGu0IKHbTkXJ2aXfImsH2V9ATh0"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """创建访问令牌"""
        try:
            # 创建完整的 JWT payload，包含所有必要字段
            payload = {}
            
            # 基本字段
            payload["jti"] = str(uuid.uuid4())  # JWT ID
            payload["sub"] = data.get("sub")     # 用户ID (subject)
            payload["iss"] = "http://localhost:8000"  # 发行者 (issuer)
            payload["aud"] = None                # 受众 (audience)
            payload["iat"] = datetime.now(timezone.utc)  # 签发时间
            
            # 过期时间
            if expires_delta:
                expire = datetime.now(timezone.utc) + expires_delta
            else:
                expire = datetime.now(timezone.utc) + timedelta(minutes=15)
            payload["exp"] = expire
            
            # 自定义字段
            payload["user_claims"] = data.get("user_claims", {})
            payload["key"] = "5462877478"  # 后端认证要求的key字段
            
            # 编码JWT
            encoded_jwt = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
            
            logger.info(f"🔐 访问令牌创建成功 - 用户ID: {data.get('sub')}, JTI: {payload['jti'][:8]}, 过期时间: {expire.isoformat()}")
            
            # 为了日志记录，创建一个可序列化的 payload 副本
            log_payload = {}
            for k, v in payload.items():
                if k == 'key':  # 跳过敏感信息
                    continue
                elif isinstance(v, datetime):
                    log_payload[k] = v.isoformat()
                else:
                    log_payload[k] = v
            
            logger.debug(f"🔍 Token payload: {json.dumps(log_payload, ensure_ascii=False)}")
            
            return encoded_jwt
        except Exception as e:
            logger.error(f"❌ 访问令牌创建失败: {str(e)}")
            raise e

    async def register(
        self,
        username: str,
        email: str,
        password: str,
        full_name: Optional[str] = None,
        personal_tags: Optional[List[str]] = None,
        long_term_goals: Optional[List[str]] = None,
        timezone: str = "Asia/Shanghai"
    ) -> RegisterResponseDto:
        """用户注册"""
        try:
            logger.info(f"开始用户注册流程 - 用户名: {username}, 邮箱: {email}")
            
            # 验证密码长度
            if len(password) < 6:
                logger.warning(f"注册失败 - 密码长度不足: {username}, 密码长度: {len(password)}")
                raise Exception("密码长度至少需要6个字符")
            
            with get_db_session() as db:
                # 检查用户名是否已存在
                existing_user = db.query(UserModel).filter(UserModel.username == username).first()
                if existing_user:
                    logger.warning(f"注册失败 - 用户名已存在: {username}")
                    raise Exception("用户名已存在")
                
                # 检查邮箱是否已存在
                existing_email = db.query(UserModel).filter(UserModel.email == email).first()
                if existing_email:
                    logger.warning(f"注册失败 - 邮箱已被注册: {email}")
                    raise Exception("邮箱已被注册")
                
                logger.info(f"用户名和邮箱检查通过 - {username}")
                
                # 创建新用户
                new_user = UserModel(
                    username=username,
                    email=email,
                    password=password,  # 实际应用中应该加密存储
                    full_name=full_name,
                    personal_tags=personal_tags,
                    long_term_goals=long_term_goals,
                    recent_focus=[],
                    daily_plan_time="08:00",
                    daily_review_time="22:00",
                    timezone=timezone,
                    status=1,  # 1: 正常
                    created_at=datetime.now()
                )
                
                logger.info(f"准备将用户信息写入数据库 - {username}")
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                
                logger.info(f"用户信息已写入数据库 - 用户ID: {new_user.id}, 用户名: {username}")
                
                # 创建访问令牌
                access_token = self.create_access_token(
                    data={"sub": str(new_user.id)},
                    expires_delta=timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
                )
                
                logger.info(f"用户注册完成 - 用户ID: {new_user.id}, 用户名: {username}")
                
                # 构建用户信息
                user_dto = UserDto(
                    id=str(new_user.id),
                    username=new_user.username,
                    email=new_user.email,
                    full_name=new_user.full_name,
                    avatar=new_user.avatar,
                    personal_tags=new_user.personal_tags or [],
                    long_term_goals=new_user.long_term_goals or [],
                    recent_focus=new_user.recent_focus or [],
                    daily_plan_time=new_user.daily_plan_time,
                    daily_review_time=new_user.daily_review_time,
                    timezone=new_user.timezone,
                    created_at=new_user.created_at.isoformat() + "Z"
                )
                
                return RegisterResponseDto(
                    access_token=access_token,
                    token_type="bearer",
                    user=user_dto,
                    expires_in=self.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                )
        except Exception as e:
            logger.error(f"用户注册失败 - 用户名: {username}, 错误: {str(e)}")
            raise e

    async def login(self, username: str, password: str) -> AuthResponseDto:
        """用户登录"""
        try:
            logger.info(f"开始用户登录流程 - 用户名: {username}")
            
            # 验证密码长度
            if len(password) < 6:
                logger.warning(f"登录失败 - 密码长度不足: {username}, 密码长度: {len(password)}")
                raise Exception("密码长度至少需要6个字符")
            
            with get_db_session() as db:
                user = db.query(UserModel).filter(UserModel.username == username).first()
                if not user:
                    logger.warning(f"登录失败 - 用户不存在: {username}")
                    raise Exception("用户不存在")
                
                logger.info(f"找到用户记录 - 用户ID: {user.id}, 用户名: {username}")
                
                if user.password != password:  # 实际应用中应该使用加密密码
                    logger.warning(f"登录失败 - 密码错误: {username}")
                    raise Exception("密码错误")
                
                if user.status != 1:
                    logger.warning(f"登录失败 - 用户已被禁用: {username}, 状态: {user.status}")
                    raise Exception("用户已被禁用")
                
                logger.info(f"用户认证通过 - 用户ID: {user.id}, 用户名: {username}")
                
                access_token = self.create_access_token(
                    data={"sub": str(user.id)},
                    expires_delta=timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
                )
                
                logger.info(f"用户登录完成 - 用户ID: {user.id}, 用户名: {username}")
                
                return AuthResponseDto(
                    access_token=access_token,
                    token_type="bearer",
                    user_id=user.id,
                    username=user.username
                )
        except Exception as e:
            logger.error(f"用户登录失败 - 用户名: {username}, 错误: {str(e)}")
            raise e

    async def get_login_user(self):
        """获取当前登录用户"""
        try:
            from auth.jwt_auth import get_jwt_auth_client
            jwt_auth = get_jwt_auth_client()
            payload = jwt_auth.get_login_payload()
            
            if not payload:
                logger.warning("获取登录用户失败 - 未找到有效的JWT payload")
                raise Exception("未登录")
            
            user_id = payload.get("sub")
            if not user_id:
                logger.warning("获取登录用户失败 - JWT payload中缺少用户ID")
                raise Exception("无效的token")
            
            logger.info(f"从JWT中获取用户ID: {user_id}")
            
            with get_db_session() as db:
                user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()
                if not user:
                    logger.warning(f"获取登录用户失败 - 数据库中未找到用户: {user_id}")
                    raise Exception("用户不存在")
                
                if user.status != 1:
                    logger.warning(f"获取登录用户失败 - 用户已被禁用: {user_id}, 状态: {user.status}")
                    raise Exception("用户已被禁用")
                
                logger.info(f"成功获取登录用户信息 - 用户ID: {user.id}, 用户名: {user.username}")
                return user
                
        except Exception as e:
            logger.error(f"获取登录用户失败: {str(e)}")
            raise e
