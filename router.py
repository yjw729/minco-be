from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uuid
import time
from datetime import datetime, timedelta
from models import (
    ApiResponse, AuthResponseDto, LoginRequestDto, RegisterRequestDto, RegisterResponseDto,
    TestConnectRequestDto, TestConnectResponseDto,
    TaskCreateDto, TaskUpdateDto, TaskDto, TaskListResponseDto, 
    RecommendationDto, RecommendationsResponseDto, AIRecommendationRequestDto,
    FocusStartDto, FocusStartResponseDto, FocusEndDto, FocusSessionDto,
    UserDto
)
from service import auth_service
from auth.jwt_auth import JWTAuthBearer
from util.logging import logger, api_logger

router = APIRouter()
auth_router = APIRouter(dependencies=[Depends(JWTAuthBearer())])

def generate_request_id() -> str:
    """生成请求追踪ID"""
    return str(uuid.uuid4())[:8]

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

def build_register_response(register_response: RegisterResponseDto):
    """构建注册响应"""
    response = api_response(data=register_response, status_code=201)
    access_token = register_response.access_token
    response.set_cookie(
        key="auth_token",
        value=access_token,
        domain=".example.com",
        max_age=604800
    )
    return response

# 认证相关路由
@router.post(
    "/auth/register",
    name="用户注册",
    response_model=ApiResponse[RegisterResponseDto],
)
async def user_register(data: RegisterRequestDto, request: Request):
    """用户注册"""
    request_id = generate_request_id()
    endpoint = "/auth/register"
    start_time = time.time()
    
    # 记录请求
    api_logger.log_request(
        endpoint=endpoint,
        method="POST", 
        data=data.dict(),
        headers=dict(request.headers),
        request_id=request_id
    )
    
    try:
        logger.info(f"[{request_id}] 开始用户注册流程，用户名: {data.username}, 邮箱: {data.email}")
        
        register_response = await auth_service.register(
            username=data.username,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            personal_tags=data.personal_tags,
            long_term_goals=data.long_term_goals,
            timezone=data.timezone
        )
        
        duration_ms = (time.time() - start_time) * 1000
        
        # 记录成功响应（脱敏token）
        response_data = register_response.dict()
        logger.info(f"[{request_id}] 用户注册成功，用户ID: {register_response.user.id}, 用时: {duration_ms:.2f}ms")
        
        api_logger.log_response(
            endpoint=endpoint,
            status_code=201,
            response_data=response_data,
            request_id=request_id,
            duration_ms=duration_ms
        )
        
        return build_register_response(register_response)
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(f"[{request_id}] 用户注册失败，用户名: {data.username}, 错误: {str(e)}, 用时: {duration_ms:.2f}ms")
        
        api_logger.log_error(
            endpoint=endpoint,
            error=e,
            request_id=request_id,
            extra_data={"username": data.username, "email": data.email}
        )
        
        api_logger.log_response(
            endpoint=endpoint,
            status_code=400,
            response_data={"error": str(e)},
            request_id=request_id,
            duration_ms=duration_ms
        )
        
        return api_response(
            data=None,
            code=400,
            message=str(e),
            status_code=400
        )

@router.post(
    "/auth/login",
    name="登录接口",
    response_model=ApiResponse[AuthResponseDto],
)
async def user_login(data: LoginRequestDto, request: Request):
    """用户登录"""
    request_id = generate_request_id()
    endpoint = "/auth/login"
    start_time = time.time()
    
    # 记录请求（脱敏密码）
    api_logger.log_request(
        endpoint=endpoint,
        method="POST",
        data={"username": data.username, "password": "***MASKED***"},
        headers=dict(request.headers),
        request_id=request_id
    )
    
    try:
        logger.info(f"[{request_id}] 开始用户登录流程，用户名: {data.username}")
        
        auth_response = await auth_service.login(username=data.username, password=data.password)
        
        duration_ms = (time.time() - start_time) * 1000
        logger.info(f"[{request_id}] 用户登录成功，用户ID: {auth_response.user_id}, 用时: {duration_ms:.2f}ms")
        
        api_logger.log_response(
            endpoint=endpoint,
            status_code=200,
            response_data=auth_response.dict(),
            request_id=request_id,
            duration_ms=duration_ms
        )
        
        return build_auth_response(auth_response)
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(f"[{request_id}] 用户登录失败，用户名: {data.username}, 错误: {str(e)}, 用时: {duration_ms:.2f}ms")
        
        api_logger.log_error(
            endpoint=endpoint,
            error=e,
            request_id=request_id,
            extra_data={"username": data.username}
        )
        
        api_logger.log_response(
            endpoint=endpoint,
            status_code=400,
            response_data={"error": str(e)},
            request_id=request_id,
            duration_ms=duration_ms
        )
        
        return api_response(
            data=None,
            code=400,
            message=str(e),
            status_code=400
        )

@auth_router.post(
    "/auth/logout",
    name="登出接口",
    response_model=ApiResponse
)
async def user_logout(request: Request):
    """用户登出"""
    request_id = generate_request_id()
    endpoint = "/auth/logout"
    start_time = time.time()
    
    api_logger.log_request(
        endpoint=endpoint,
        method="POST",
        headers=dict(request.headers),
        request_id=request_id
    )
    
    try:
        user = await auth_service.get_login_user()
        duration_ms = (time.time() - start_time) * 1000
        
        logger.info(f"[{request_id}] 用户登出成功，用户ID: {user.id}, 用时: {duration_ms:.2f}ms")
        
        api_logger.log_response(
            endpoint=endpoint,
            status_code=200,
            response_data=[],
            request_id=request_id,
            duration_ms=duration_ms
        )
        
        return api_response(data=[])
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(f"[{request_id}] 用户登出失败，错误: {str(e)}, 用时: {duration_ms:.2f}ms")
        
        api_logger.log_error(endpoint=endpoint, error=e, request_id=request_id)
        return api_response(data=None, code=400, message=str(e), status_code=400)

# 测试相关路由
@router.post(
    "/test/connect_test",
    name="测试连接接口",
    response_model=ApiResponse[TestConnectResponseDto],
)
async def test_connect(data: TestConnectRequestDto, request: Request):
    """测试连接"""
    request_id = generate_request_id()
    endpoint = "/test/connect_test"
    start_time = time.time()
    
    api_logger.log_request(
        endpoint=endpoint,
        method="POST",
        data=data.dict(),
        headers=dict(request.headers),
        request_id=request_id
    )
    
    try:
        logger.info(f"[{request_id}] 收到连接测试请求，UUID: {data.uuid}")
        
        response_data = TestConnectResponseDto(
            status="success",
            message="Connection successful",
            uuid=data.uuid
        )
        
        duration_ms = (time.time() - start_time) * 1000
        logger.info(f"[{request_id}] 连接测试成功，用时: {duration_ms:.2f}ms")
        
        api_logger.log_response(
            endpoint=endpoint,
            status_code=200,
            response_data=response_data.dict(),
            request_id=request_id,
            duration_ms=duration_ms
        )
        
        return api_response(data=response_data)
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(f"[{request_id}] 连接测试失败，错误: {str(e)}, 用时: {duration_ms:.2f}ms")
        
        api_logger.log_error(endpoint=endpoint, error=e, request_id=request_id)
        return api_response(data=None, code=500, message=str(e), status_code=500)

# ==================== P0 事项管理接口 ====================

@auth_router.post(
    "/items",
    name="创建事项",
    response_model=ApiResponse[TaskDto],
)
async def create_task(data: TaskCreateDto, request: Request):
    """创建新事项"""
    request_id = generate_request_id()
    endpoint = "/items"
    start_time = time.time()
    
    api_logger.log_request(
        endpoint=endpoint,
        method="POST",
        data=data.dict(),
        headers=dict(request.headers),
        request_id=request_id
    )
    
    try:
        logger.info(f"[{request_id}] 开始创建事项，标题: {data.title}, 分类: {data.category_id}")
        
        # 模拟创建事项
        task_id = str(uuid.uuid4())
        current_time = datetime.now().isoformat() + "Z"
        
        task = TaskDto(
            id=task_id,
            title=data.title,
            description=data.description,
            emoji=data.emoji,
            category_id=data.category_id,
            project_id=data.project_id,
            start_time=data.start_time,
            end_time=data.end_time,
            estimated_duration=data.estimated_duration,
            time_slot_id=data.time_slot_id,
            priority=data.priority,
            status_id=data.status_id or 1,
            sub_tasks=data.sub_tasks or [],
            created_at=current_time,
            updated_at=current_time
        )
        
        duration_ms = (time.time() - start_time) * 1000
        logger.info(f"[{request_id}] 事项创建成功，任务ID: {task.id}, 用时: {duration_ms:.2f}ms")
        
        api_logger.log_response(
            endpoint=endpoint,
            status_code=201,
            response_data=task.dict(),
            request_id=request_id,
            duration_ms=duration_ms
        )
        
        return api_response(data=task, status_code=201)
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(f"[{request_id}] 事项创建失败，标题: {data.title}, 错误: {str(e)}, 用时: {duration_ms:.2f}ms")
        
        api_logger.log_error(
            endpoint=endpoint,
            error=e,
            request_id=request_id,
            extra_data={"title": data.title, "category_id": data.category_id}
        )
        
        return api_response(data=None, code=500, message=str(e), status_code=500)

@auth_router.get(
    "/items",
    name="获取事项列表",
    response_model=ApiResponse[TaskListResponseDto],
)
async def get_tasks(
    request: Request,
    date: Optional[str] = Query(None, description="筛选日期 YYYY-MM-DD"),
    project_id: Optional[str] = Query(None, description="项目ID"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    status_id: Optional[int] = Query(None, description="状态ID"),
    priority: Optional[int] = Query(None, description="优先级"),
    is_completed: Optional[bool] = Query(None, description="是否完成"),
    time_slot_id: Optional[int] = Query(None, description="时间段ID"),
    sort_by: Optional[str] = Query("created_at", description="排序字段"),
    order: Optional[str] = Query("desc", description="排序顺序"),
    page: int = Query(1, description="页码"),
    limit: int = Query(20, description="每页数量")
):
    """获取事项列表，支持筛选和分页"""
    request_id = generate_request_id()
    endpoint = "/items"
    start_time = time.time()
    
    # 构建查询参数
    query_params = {
        "date": date,
        "project_id": project_id,
        "category_id": category_id,
        "status_id": status_id,
        "priority": priority,
        "is_completed": is_completed,
        "time_slot_id": time_slot_id,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit
    }
    
    api_logger.log_request(
        endpoint=endpoint,
        method="GET",
        params=query_params,
        headers=dict(request.headers),
        request_id=request_id
    )
    
    try:
        logger.info(f"[{request_id}] 开始获取事项列表，分类: {category_id}, 状态: {status_id}, 页码: {page}")
        
        # 模拟数据
        mock_tasks = [
            TaskDto(
                id=str(uuid.uuid4()),
                title="完成项目文档",
                description="编写详细的API文档",
                emoji="📝",
                category_id=3,  # 工作
                priority=4,
                status_id=1,  # pending
                created_at=datetime.now().isoformat() + "Z",
                updated_at=datetime.now().isoformat() + "Z"
            ),
            TaskDto(
                id=str(uuid.uuid4()),
                title="健身锻炼",
                description="有氧运动30分钟",
                emoji="💪",
                category_id=2,  # 健康
                priority=3,
                status_id=1,
                created_at=datetime.now().isoformat() + "Z",
                updated_at=datetime.now().isoformat() + "Z"
            )
        ]
        
        # 应用筛选逻辑（简化示例）
        filtered_tasks = mock_tasks
        if category_id:
            filtered_tasks = [t for t in filtered_tasks if t.category_id == category_id]
        if status_id:
            filtered_tasks = [t for t in filtered_tasks if t.status_id == status_id]
        
        response_data = TaskListResponseDto(
            items=filtered_tasks,
            pagination={
                "total_items": len(filtered_tasks),
                "total_pages": 1,
                "current_page": page,
                "limit": limit
            }
        )
        
        duration_ms = (time.time() - start_time) * 1000
        logger.info(f"[{request_id}] 事项列表获取成功，返回 {len(filtered_tasks)} 个事项, 用时: {duration_ms:.2f}ms")
        
        api_logger.log_response(
            endpoint=endpoint,
            status_code=200,
            response_data={"items_count": len(filtered_tasks), "pagination": response_data.pagination},
            request_id=request_id,
            duration_ms=duration_ms
        )
        
        return api_response(data=response_data)
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(f"[{request_id}] 事项列表获取失败，错误: {str(e)}, 用时: {duration_ms:.2f}ms")
        
        api_logger.log_error(
            endpoint=endpoint,
            error=e,
            request_id=request_id,
            extra_data=query_params
        )
        
        return api_response(data=None, code=500, message=str(e), status_code=500)

@auth_router.get(
    "/items/{item_id}",
    name="获取单个事项",
    response_model=ApiResponse[TaskDto],
)
async def get_task(item_id: str = Path(..., description="事项ID")):
    """获取单个事项详情"""
    # 模拟获取事项
    task = TaskDto(
        id=item_id,
        title="示例事项",
        description="这是一个示例事项的详细描述",
        emoji="📋",
        category_id=1,
        priority=3,
        status_id=1,
        created_at=datetime.now().isoformat() + "Z",
        updated_at=datetime.now().isoformat() + "Z"
    )
    
    return api_response(data=task)

@auth_router.put(
    "/items/{item_id}",
    name="更新事项",
    response_model=ApiResponse[TaskDto],
)
async def update_task(item_id: str, data: TaskUpdateDto):
    """更新事项信息"""
    # 模拟更新事项
    current_time = datetime.now().isoformat() + "Z"
    
    updated_task = TaskDto(
        id=item_id,
        title=data.title or "更新后的事项标题",
        description=data.description,
        emoji=data.emoji,
        category_id=data.category_id or 1,
        project_id=data.project_id,
        start_time=data.start_time,
        end_time=data.end_time,
        estimated_duration=data.estimated_duration,
        time_slot_id=data.time_slot_id,
        priority=data.priority or 3,
        status_id=data.status_id or 1,
        sub_tasks=data.sub_tasks or [],
        created_at="2024-05-24T09:00:00Z",  # 保持原创建时间
        updated_at=current_time
    )
    
    logger.info(f"Updated task: {item_id}")
    return api_response(data=updated_task)

@auth_router.delete(
    "/items/{item_id}",
    name="删除事项",
)
async def delete_task(item_id: str):
    """删除事项"""
    logger.info(f"Deleted task: {item_id}")
    return JSONResponse(content="", status_code=204)

# ==================== P0 AI功能接口 ====================

@auth_router.post(
    "/ai/recommendations",
    name="智能推荐",
    response_model=ApiResponse[RecommendationsResponseDto],
)
async def get_ai_recommendations(data: AIRecommendationRequestDto):
    """获取AI智能推荐"""
    # 模拟AI推荐
    mock_task = TaskDto(
        id=str(uuid.uuid4()),
        title="处理重要邮件",
        description="回复客户咨询邮件",
        emoji="📧",
        category_id=3,  # 工作
        priority=4,
        status_id=1,
        created_at=datetime.now().isoformat() + "Z",
        updated_at=datetime.now().isoformat() + "Z"
    )
    
    recommendations = RecommendationsResponseDto(
        recommendations=[
            RecommendationDto(
                item=mock_task,
                reason="现在是上午，精力充沛，适合处理重要工作",
                confidence_score=0.85
            )
        ],
        message="基于您的当前状态和任务优先级，为您推荐以下事项"
    )
    
    return api_response(data=recommendations)

# ==================== P0 专注功能接口 ====================

@auth_router.post(
    "/focus/start",
    name="开始专注",
    response_model=ApiResponse[FocusStartResponseDto],
)
async def start_focus(data: FocusStartDto):
    """开始专注模式"""
    session_id = str(uuid.uuid4())
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=data.duration)
    
    # 获取关联的任务（模拟）
    task = TaskDto(
        id=data.task_id,
        title="专注任务",
        description="当前正在专注的任务",
        emoji="🎯",
        category_id=1,
        priority=4,
        status_id=2,  # in_progress
        created_at=datetime.now().isoformat() + "Z",
        updated_at=datetime.now().isoformat() + "Z"
    )
    
    response_data = FocusStartResponseDto(
        session_id=session_id,
        start_time=start_time.isoformat() + "Z",
        end_time=end_time.isoformat() + "Z",
        task=task
    )
    
    logger.info(f"Started focus session: {session_id} for task: {data.task_id}")
    return api_response(data=response_data)

@auth_router.post(
    "/focus/{session_id}/end",
    name="结束专注",
    response_model=ApiResponse[FocusSessionDto],
)
async def end_focus(session_id: str, data: FocusEndDto):
    """结束专注会话"""
    current_time = datetime.now().isoformat() + "Z"
    
    session = FocusSessionDto(
        id=session_id,
        task_id="sample-task-id",
        start_time="2024-05-24T09:00:00Z",
        end_time=current_time,
        planned_duration=1800,  # 30分钟
        actual_duration=data.actual_duration,
        mode_id=1,  # pomodoro
        completed=data.completed,
        interruptions=data.interruptions
    )
    
    logger.info(f"Ended focus session: {session_id}, completed: {data.completed}")
    return api_response(data=session)

# ==================== P0 用户信息接口 ====================

@auth_router.get(
    "/user/profile",
    name="获取用户信息",
    response_model=ApiResponse[UserDto],
)
async def get_user_profile():
    """获取用户基础信息"""
    # 模拟用户信息
    user = UserDto(
        id=str(uuid.uuid4()),
        username="demo_user",
        email="demo@example.com",
        full_name="演示用户",
        avatar="https://avatar.example.com/demo.jpg",
        personal_tags=["MBTI-INFP", "夜猫子"],
        long_term_goals=["身体健康", "职业发展"],
        recent_focus=["写论文", "学习编程"],
        daily_plan_time="08:00",
        daily_review_time="22:00",
        timezone="Asia/Shanghai",
        created_at=datetime.now().isoformat() + "Z"
    )
    
    return api_response(data=user)
