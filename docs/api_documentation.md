# Minco BE API 接口文档

## 📋 概述

**项目名称**: minco BE  
**版本**: v0.0.1  
**基础URL**: `http://localhost:8000/api/v1`  
**框架**: FastAPI  

## 🔧 统一响应格式

所有接口都遵循统一的响应格式：

```json
{
    "code": 0,           // 业务状态码，0表示成功
    "message": "success", // 响应消息
    "data": {}           // 实际数据载荷
}
```

## 🔐 认证说明

- **无需认证**: 直接访问的接口
- **需要认证**: 需要在请求头中携带 `Authorization: Bearer <token>` 或通过Cookie传递认证信息

---

## 📚 接口列表

### 1. 用户认证

#### 1.1 用户登录

- **接口名称**: 用户登录
- **URL**: `/api/v1/auth/login`
- **方法**: `POST`
- **认证**: 无需认证
- **描述**: 用户登录获取访问令牌

**请求参数**:
```json
{
    "username": "用户名",
    "password": "密码"
}
```

**请求示例**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
         "username": "admin",
         "password": "123456"
     }'
```

**成功响应**:
```json
{
    "code": 0,
    "message": "success",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "user_id": 1,
        "username": "admin"
    }
}
```

**注意**: 登录成功后会自动设置 `auth_token` Cookie（有效期7天）

#### 1.2 用户登出

- **接口名称**: 用户登出
- **URL**: `/api/v1/auth/logout`
- **方法**: `POST`
- **认证**: 需要认证
- **描述**: 用户登出系统

**请求示例**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
     -H "Authorization: Bearer <your_token>"
```

**成功响应**:
```json
{
    "code": 0,
    "message": "success",
    "data": []
}
```

### 2. 系统测试

#### 2.1 连接测试

- **接口名称**: 测试连接
- **URL**: `/api/v1/test/connect_test`
- **方法**: `POST`
- **认证**: 无需认证
- **描述**: 测试系统连接状态

**请求参数**:
```json
{
    "uuid": "user-uuid-optional"  // 可选参数
}
```

**请求示例**:
```bash
curl -X POST "http://localhost:8000/api/v1/test/connect_test" \
     -H "Content-Type: application/json" \
     -d '{
         "uuid": "test-uuid-123"
     }'
```

**成功响应**:
```json
{
    "code": 0,
    "message": "success",
    "data": {
        "status": "success",
        "message": "Connection successful",
        "uuid": "test-uuid-123"
    }
}
```

---

## 📊 数据模型

### ApiResponse (统一响应格式)
```typescript
interface ApiResponse<T> {
    code: number;        // 业务状态码
    message: string;     // 响应消息
    data: T | null;      // 数据载荷
}
```

### LoginRequestDto (登录请求)
```typescript
interface LoginRequestDto {
    username: string;    // 用户名
    password: string;    // 密码
}
```

### AuthResponseDto (认证响应)
```typescript
interface AuthResponseDto {
    access_token: string;   // 访问令牌
    token_type: string;     // 令牌类型，默认"bearer"
    user_id: number;        // 用户ID
    username: string;       // 用户名
}
```

### TestConnectRequestDto (测试连接请求)
```typescript
interface TestConnectRequestDto {
    uuid?: string;       // 可选的用户UUID
}
```

### TestConnectResponseDto (测试连接响应)
```typescript
interface TestConnectResponseDto {
    status: string;      // 状态
    message: string;     // 消息
    uuid?: string;       // 用户UUID（如果提供）
}
```

---

## 🚀 快速开始

### 1. 启动服务器
```bash
uvicorn main:app --reload
```

### 2. 访问API文档
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. 测试接口
```bash
# 测试连接
curl -X POST "http://localhost:8000/api/v1/test/connect_test" \
     -H "Content-Type: application/json" \
     -d '{"uuid": "test"}'

# 用户登录
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "123456"}'
```

---

## 🎯 错误处理

### 常见错误码

| 状态码 | 含义 | 说明 |
|--------|------|------|
| 0 | 成功 | 请求处理成功 |
| 1001 | 参数错误 | 请求参数格式不正确 |
| 1002 | 认证失败 | 用户名或密码错误 |
| 1003 | 权限不足 | 需要登录或权限不够 |
| 5000 | 服务器错误 | 内部服务器错误 |

### 错误响应示例
```json
{
    "code": 1002,
    "message": "用户名或密码错误",
    "data": []
}
```

---

## 🔧 开发说明

### 技术栈
- **后端框架**: FastAPI
- **数据验证**: Pydantic
- **认证**: JWT
- **数据库**: MySQL
- **异步支持**: asyncio

### 项目结构
```
minco-be/
├── main.py              # 应用入口
├── router.py            # 路由定义
├── models.py            # 数据模型
├── auth/                # 认证相关
├── service/             # 业务逻辑
├── util/                # 工具函数
└── docs/                # 接口文档
```

### 添加新接口
1. 在 `models.py` 中定义请求/响应模型
2. 在 `router.py` 中添加路由处理函数
3. 更新接口文档

---

*文档生成时间: 2024年12月*  
*更新记录: 包含登录、登出和测试连接接口* 