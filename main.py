from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from router import router, auth_router

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

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """根路径，返回API基本信息"""
    return {
        "message": "欢迎使用 minco BE API",
        "version": "0.0.1",
        "docs": "/docs",
        "redoc": "/redoc",
        "api_prefix": "/api/v1"
    }

# 注册路由
app.include_router(router, prefix="/api/v1", tags=["API"])
app.include_router(auth_router, prefix="/api/v1", tags=["认证"])