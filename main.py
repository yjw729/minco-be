from fastapi import FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from router import router, auth_router
from util.logging import logger, api_logger
import logging
import sys
import os
import time
import uuid
from datetime import datetime

# 设置日志级别为DEBUG以获取更详细的信息
logging.getLogger().setLevel(logging.INFO)
logger.info("="*60)
logger.info("🚀 Minco BE 服务启动中...")
logger.info(f"📅 启动时间: {datetime.now().isoformat()}")
logger.info(f"🐍 Python版本: {sys.version}")
logger.info(f"📂 工作目录: {os.getcwd()}")
logger.info("="*60)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """HTTP请求日志中间件"""
    
    async def dispatch(self, request: Request, call_next):
        # 生成请求ID
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        
        # 获取客户端信息
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # 记录请求开始
        logger.info(
            f"🔵 [REQUEST_START] {request_id} | "
            f"{request.method} {request.url} | "
            f"客户端: {client_ip} | "
            f"User-Agent: {user_agent[:50]}..."
        )
        
        # 处理请求
        try:
            response = await call_next(request) 
            duration_ms = (time.time() - start_time) * 1000
            
            # 记录请求完成
            status_emoji = "🟢" if response.status_code < 400 else "🟡" if response.status_code < 500 else "🔴"
            logger.info(
                f"{status_emoji} [REQUEST_END] {request_id} | "
                f"{request.method} {request.url} | "
                f"状态码: {response.status_code} | "
                f"耗时: {duration_ms:.2f}ms"
            )
            
            return response
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                f"❌ [REQUEST_ERROR] {request_id} | "
                f"{request.method} {request.url} | "
                f"错误: {str(e)} | "
                f"耗时: {duration_ms:.2f}ms"
            )
            raise

app = FastAPI(
    title="minco BE 🚀🚀🚀",
    description="minco BE is based on FastAPI framework. 🚀🚀🚀",
    version="0.0.1",
    terms_of_service="https://mindco.com",
    contact={
        "name": "MAC team",
        "url": "https://mindco.com",
        "email": "test@mindco.com",
    },
)

# 添加请求日志中间件（在CORS之前）
app.add_middleware(RequestLoggingMiddleware)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("✅ 中间件已配置:")
logger.info("  - 请求日志中间件：自动记录所有HTTP请求")
logger.info("  - CORS中间件：允许所有来源跨域访问")

@app.get("/")
async def root():
    """根路径，返回API基本信息"""
    logger.info("🏠 处理根路径请求")
    return {
        "message": "欢迎使用 minco BE API",
        "version": "0.0.1",
        "docs": "/docs",
        "redoc": "/redoc",
        "api_prefix": "/api/v1",
        "timestamp": datetime.now().isoformat()
    }

# 注册路由
app.include_router(router, prefix="/api/v1", tags=["API"])
app.include_router(auth_router, prefix="/api/v1", tags=["认证"])

logger.info("📚 API路由已注册:")
logger.info("  - 公共路由: /api/v1/...")
logger.info("  - 认证路由: /api/v1/... (需要JWT)")
logger.info("🔗 API文档地址: http://localhost:8000/docs")
logger.info("🌟 Minco BE 服务启动完成，等待请求...")

# 应用程序启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info("🎉 应用程序启动事件触发")
    logger.info("💾 检查数据库连接...")
    # 这里可以添加数据库连接测试等启动检查
    logger.info("✅ 应用程序启动完成")

@app.on_event("shutdown") 
async def shutdown_event():
    """应用关闭时执行"""
    logger.info("👋 应用程序正在关闭...")
    logger.info("🧹 清理资源...")
    logger.info("✅ 应用程序已安全关闭")