from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    """API统一响应格式"""
    code: int = 0
    message: str = "success"
    data: Optional[T] = None

# 用户相关模型
class UserDto(BaseModel):
    """用户信息模型"""
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    avatar: Optional[str] = None
    personal_tags: Optional[List[str]] = None
    long_term_goals: Optional[List[str]] = None
    recent_focus: Optional[List[str]] = None
    daily_plan_time: Optional[str] = None
    daily_review_time: Optional[str] = None
    timezone: Optional[str] = None
    created_at: str

class LoginRequestDto(BaseModel):
    """登录请求"""
    username: str = Field(..., min_length=1, description="用户名")
    password: str = Field(..., min_length=6, description="密码，最少6个字符")

class RegisterRequestDto(BaseModel):
    """注册请求"""
    username: str = Field(..., min_length=1, description="用户名")
    email: str = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=6, description="密码，最少6个字符")
    full_name: Optional[str] = None
    personal_tags: Optional[List[str]] = None
    long_term_goals: Optional[List[str]] = None
    timezone: Optional[str] = "Asia/Shanghai"

class RegisterResponseDto(BaseModel):
    """注册响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserDto
    expires_in: int

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

# 事项相关模型
class TaskCreateDto(BaseModel):
    """创建事项请求"""
    title: str
    description: Optional[str] = None
    emoji: Optional[str] = None
    category_id: int
    project_id: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    estimated_duration: Optional[int] = None
    time_slot_id: Optional[int] = None
    priority: int
    status_id: Optional[int] = 1
    sub_tasks: Optional[List[str]] = None

class TaskUpdateDto(BaseModel):
    """更新事项请求"""
    title: Optional[str] = None
    description: Optional[str] = None
    emoji: Optional[str] = None
    category_id: Optional[int] = None
    project_id: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    estimated_duration: Optional[int] = None
    time_slot_id: Optional[int] = None
    priority: Optional[int] = None
    status_id: Optional[int] = None
    sub_tasks: Optional[List[str]] = None

class TaskDto(BaseModel):
    """事项数据模型"""
    id: str
    title: str
    description: Optional[str] = None
    emoji: Optional[str] = None
    category_id: int
    project_id: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    estimated_duration: Optional[int] = None
    time_slot_id: Optional[int] = None
    priority: int
    status_id: int
    is_overdue: bool = False
    sub_tasks: Optional[List[str]] = None
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None

class TaskListResponseDto(BaseModel):
    """事项列表响应"""
    items: List[TaskDto]
    pagination: dict

class RecommendationDto(BaseModel):
    """推荐事项"""
    item: TaskDto
    reason: str
    confidence_score: Optional[float] = None

class RecommendationsResponseDto(BaseModel):
    """智能推荐响应"""
    recommendations: List[RecommendationDto]
    message: Optional[str] = None

# 专注相关模型
class FocusStartDto(BaseModel):
    """开始专注请求"""
    task_id: str
    duration: int  # 秒
    mode: str  # "pomodoro" 或 "free"

class FocusSessionDto(BaseModel):
    """专注会话模型"""
    id: str
    task_id: str
    start_time: str
    end_time: Optional[str] = None
    planned_duration: int
    actual_duration: Optional[int] = None
    mode_id: int
    completed: bool = False
    interruptions: Optional[int] = None

class FocusStartResponseDto(BaseModel):
    """开始专注响应"""
    session_id: str
    start_time: str
    end_time: str
    task: TaskDto

class FocusEndDto(BaseModel):
    """结束专注请求"""
    actual_duration: int
    completed: bool
    interruptions: Optional[int] = None

# AI推荐请求
class AIRecommendationRequestDto(BaseModel):
    """AI推荐请求"""
    context: Optional[str] = None
    user_mood: Optional[str] = None
    available_time_minutes: Optional[int] = None
