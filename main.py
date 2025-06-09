from fastapi import FastAPI
from router import router, auth_router

app = FastAPI(
    title="minco BE",
    description="基于FastAPI的minco BE",
    version="1.0.0"
)

# 注册路由
app.include_router(router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")