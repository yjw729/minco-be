# API 接口概览

## 基础信息
- **基础URL**: `http://localhost:8000/api/v1`
- **认证方式**: JWT Token / Cookie
- **数据格式**: JSON

## 接口列表

### 🔐 认证相关
| 接口 | 方法 | URL | 认证 | 描述 |
|------|------|-----|------|------|
| 用户登录 | POST | `/auth/login` | ❌ | 用户登录获取访问令牌 |
| 用户登出 | POST | `/auth/logout` | ✅ | 用户登出系统 |

### 🔧 系统测试
| 接口 | 方法 | URL | 认证 | 描述 |
|------|------|-----|------|------|
| 连接测试 | POST | `/test/connect_test` | ❌ | 测试系统连接状态 |

## 响应格式

```json
{
    "code": 0,
    "message": "success",
    "data": {}
}
```

## 快速测试

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