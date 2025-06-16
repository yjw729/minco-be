# Minco BE API 接口概览

> **📅 最后更新**: 2024年12月  
> **🎯 状态**: 核心功能已实现，密码验证已加强  
> **📋 版本**: v1.0

## 🚀 基础信息

### 环境配置
- **🏠 开发环境**: `http://localhost:8000/api/v1`
- **🌍 生产环境**: `https://api.minco.app/api/v1`
- **🔐 认证方式**: JWT Token (Bearer) / Cookie
- **📦 数据格式**: JSON
- **⏰ Token有效期**: 30分钟
- **🔒 密码要求**: 最少6个字符

### 统一响应格式
```json
{
    "code": 0,
    "message": "success", 
    "data": {
        // 实际数据内容
    }
}
```

## 📋 接口列表

### 🔐 认证相关
| 接口 | 方法 | URL | 认证 | 实现状态 | 描述 |
|------|------|-----|------|----------|------|
| 用户注册 | POST | `/auth/register` | ❌ | ✅ | 用户注册账号（密码≥6字符） |
| 用户登录 | POST | `/auth/login` | ❌ | ✅ | 用户登录获取访问令牌 |
| 用户登出 | POST | `/auth/logout` | ✅ | ✅ | 用户登出系统 |

### 🔧 系统测试
| 接口 | 方法 | URL | 认证 | 实现状态 | 描述 |
|------|------|-----|------|----------|------|
| 连接测试 | POST | `/test/connect_test` | ❌ | ✅ | 测试系统连接状态 |

### 📋 事项管理
| 接口 | 方法 | URL | 认证 | 实现状态 | 描述 |
|------|------|-----|------|----------|------|
| 创建事项 | POST | `/items` | ✅ | ✅ | 创建新的事项 |
| 获取事项列表 | GET | `/items` | ✅ | ✅ | 获取事项列表，支持筛选和分页 |
| 获取单个事项 | GET | `/items/{itemId}` | ✅ | ✅ | 获取指定事项详情 |
| 更新事项 | PUT | `/items/{itemId}` | ✅ | ✅ | 更新指定事项信息 |
| 删除事项 | DELETE | `/items/{itemId}` | ✅ | ✅ | 删除指定事项 |

### 🤖 AI功能
| 接口 | 方法 | URL | 认证 | 实现状态 | 描述 |
|------|------|-----|------|----------|------|
| 智能推荐 | POST | `/ai/recommendations` | ✅ | ✅ | 获取AI智能推荐 |

### 🎯 专注功能
| 接口 | 方法 | URL | 认证 | 实现状态 | 描述 |
|------|------|-----|------|----------|------|
| 开始专注 | POST | `/focus/start` | ✅ | ✅ | 开始专注模式 |
| 结束专注 | POST | `/focus/{sessionId}/end` | ✅ | ✅ | 结束专注会话 |

### 👤 用户信息
| 接口 | 方法 | URL | 认证 | 实现状态 | 描述 |
|------|------|-----|------|----------|------|
| 获取用户信息 | GET | `/user/profile` | ✅ | ✅ | 获取用户基础信息 |

## 🧪 快速测试指南

### 🌍 生产环境测试

#### 1. 🔗 连接测试（推荐首先测试）
```bash
curl -X POST "https://api.minco.app/api/v1/test/connect_test" \
     -H "Content-Type: application/json" \
     -d '{"uuid": "frontend-test-'$(date +%s)'"}'
```

```javascript
// JavaScript 前端测试
fetch('https://api.minco.app/api/v1/test/connect_test', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        uuid: 'frontend-test-' + Date.now()
    })
})
.then(response => response.json())
.then(data => console.log('✅ 连接成功:', data))
.catch(error => console.error('❌ 连接失败:', error));
```

#### 2. 🔐 用户注册（新增密码验证）
```bash
curl -X POST "https://api.minco.app/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com", 
       "password": "password123",
       "full_name": "测试用户"
     }'
```

```javascript
// JavaScript 注册示例
fetch('https://api.minco.app/api/v1/auth/register', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'testuser',
        email: 'test@example.com',
        password: 'password123', // 至少6个字符
        full_name: '测试用户'
    })
})
.then(response => response.json())
.then(data => {
    if (data.code === 0) {
        localStorage.setItem('access_token', data.data.access_token);
        console.log('✅ 注册成功:', data);
    } else {
        console.error('❌ 注册失败:', data.message);
    }
})
.catch(error => console.error('❌ 网络错误:', error));
```

#### 3. 🔑 用户登录
```bash
curl -X POST "https://api.minco.app/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "password123"}'
```

```javascript
// JavaScript 登录示例
fetch('https://api.minco.app/api/v1/auth/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'testuser',
        password: 'password123' // 至少6个字符
    })
})
.then(response => response.json())
.then(data => {
    if (data.code === 0) {
        localStorage.setItem('access_token', data.data.access_token);
        console.log('✅ 登录成功:', data);
    } else {
        console.error('❌ 登录失败:', data.message);
    }
})
.catch(error => console.error('❌ 网络错误:', error));
```

#### 4. 📝 创建事项（需要认证）
```bash
curl -X POST "https://api.minco.app/api/v1/items" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "测试事项",
       "description": "这是一个测试事项",
       "emoji": "📝",
       "category_id": 1,
       "priority": 3
     }'
```

```javascript
// JavaScript 创建事项示例
const token = localStorage.getItem('access_token');
fetch('https://api.minco.app/api/v1/items', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        title: '测试事项',
        description: '这是一个测试事项',
        emoji: '📝',
        category_id: 1,
        priority: 3
    })
})
.then(response => response.json())
.then(data => {
    if (data.code === 0) {
        console.log('✅ 事项创建成功:', data);
    } else {
        console.error('❌ 创建失败:', data.message);
    }
})
.catch(error => console.error('❌ 网络错误:', error));
```

#### 5. 📋 获取事项列表（需要认证）
```bash
curl -X GET "https://api.minco.app/api/v1/items?page=1&limit=10" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

```javascript
// JavaScript 获取事项列表示例
const token = localStorage.getItem('access_token');
fetch('https://api.minco.app/api/v1/items?page=1&limit=10', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${token}`,
    }
})
.then(response => response.json())
.then(data => {
    if (data.code === 0) {
        console.log('✅ 事项列表:', data);
    } else {
        console.error('❌ 获取失败:', data.message);
    }
})
.catch(error => console.error('❌ 网络错误:', error));
```

### 🏠 本地开发环境测试

将上述示例中的 `https://api.minco.app` 替换为 `http://localhost:8000` 即可用于本地测试。

## 📊 数据字典

### 分类ID (category_id)
- `1`: 生活 🏠
- `2`: 健康 💪  
- `3`: 工作 💼
- `4`: 学习 📚
- `5`: 放松 😌
- `6`: 探索 🔍

### 状态ID (status_id)
- `1`: pending (待处理) ⏳
- `2`: in_progress (进行中) 🔄
- `3`: completed (已完成) ✅
- `4`: cancelled (已取消) ❌

### 时间段ID (time_slot_id)
- `1`: 上午 🌅
- `2`: 中午 ☀️
- `3`: 下午 🌤️
- `4`: 晚上 🌙
- `5`: 随时 ⏰

### 优先级 (priority)
- `1`: 最低 🟢
- `2`: 较低 🟡
- `3`: 中等 🟠
- `4`: 较高 🔴
- `5`: 最高 🔥

## ⚠️ 重要说明

### 🔗 URL格式
- ✅ **正确**: `https://api.minco.app/api/v1/test/connect_test`
- ❌ **错误**: `https://api.minco.app/v1/test/connect_test`

### 🔐 密码安全要求
- **最少长度**: 6个字符
- **验证层级**: Pydantic字段验证 + 业务逻辑验证
- **错误提示**: "密码长度至少需要6个字符"

### 🏷️ 认证标记说明
- ❌ = 无需认证
- ✅ = 需要JWT Token认证

### 📋 请求要求
1. **认证接口**: 必须包含 `Authorization: Bearer {token}` 头
2. **内容类型**: 所有POST/PUT请求需设置 `Content-Type: application/json`
3. **Token过期**: 30分钟后需重新登录

### 🧪 推荐测试顺序
1. 🔗 连接测试 (`/test/connect_test`)
2. 🔐 用户注册 (`/auth/register`) 
3. 🔑 用户登录 (`/auth/login`)
4. 📝 其他需要认证的接口

## 📱 前端集成示例

```javascript
// 完整的API客户端封装
class MincoAPI {
    constructor(baseURL = 'https://api.minco.app/api/v1') {
        this.baseURL = baseURL;
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const token = localStorage.getItem('access_token');
        
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` }),
                ...options.headers
            },
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            // 统一处理响应
            if (data.code === 0) {
                return data;
            } else {
                throw new Error(data.message || '请求失败');
            }
        } catch (error) {
            console.error(`API请求失败 [${endpoint}]:`, error);
            throw error;
        }
    }
    
    // 🔗 测试连接
    testConnection() {
        return this.request('/test/connect_test', {
            method: 'POST',
            body: JSON.stringify({ uuid: 'test-' + Date.now() })
        });
    }
    
    // 🔐 用户注册
    register(userData) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }
    
    // 🔑 用户登录
    login(username, password) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
    }
    
    // 🔓 用户登出
    logout() {
        return this.request('/auth/logout', {
            method: 'POST'
        });
    }
    
    // 📋 获取事项列表
    getTasks(params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request(`/items${query ? '?' + query : ''}`);
    }
    
    // 📝 创建事项
    createTask(taskData) {
        return this.request('/items', {
            method: 'POST',
            body: JSON.stringify(taskData)
        });
    }
    
    // 📄 获取单个事项
    getTask(taskId) {
        return this.request(`/items/${taskId}`);
    }
    
    // ✏️ 更新事项
    updateTask(taskId, taskData) {
        return this.request(`/items/${taskId}`, {
            method: 'PUT',
            body: JSON.stringify(taskData)
        });
    }
    
    // 🗑️ 删除事项
    deleteTask(taskId) {
        return this.request(`/items/${taskId}`, {
            method: 'DELETE'
        });
    }
    
    // 🤖 获取AI推荐
    getAIRecommendations(requestData) {
        return this.request('/ai/recommendations', {
            method: 'POST',
            body: JSON.stringify(requestData)
        });
    }
    
    // 🎯 开始专注
    startFocus(focusData) {
        return this.request('/focus/start', {
            method: 'POST',
            body: JSON.stringify(focusData)
        });
    }
    
    // ⏹️ 结束专注
    endFocus(sessionId, endData) {
        return this.request(`/focus/${sessionId}/end`, {
            method: 'POST',
            body: JSON.stringify(endData)
        });
    }
    
    // 👤 获取用户信息
    getUserProfile() {
        return this.request('/user/profile');
    }
}

// 使用示例
const api = new MincoAPI();

// 完整的使用流程
async function quickTest() {
    try {
        // 1. 测试连接
        console.log('🔗 测试连接...');
        await api.testConnection();
        console.log('✅ 连接正常');
        
        // 2. 注册用户
        console.log('🔐 注册用户...');
        await api.register({
            username: 'testuser',
            email: 'test@example.com',
            password: 'password123',
            full_name: '测试用户'
        });
        console.log('✅ 注册成功');
        
        // 3. 创建事项
        console.log('📝 创建事项...');
        const task = await api.createTask({
            title: '测试事项',
            description: '这是一个测试事项',
            emoji: '📝',
            category_id: 1,
            priority: 3
        });
        console.log('✅ 事项创建成功:', task.data);
        
        // 4. 获取事项列表
        console.log('📋 获取事项列表...');
        const tasks = await api.getTasks({ page: 1, limit: 10 });
        console.log('✅ 事项列表:', tasks.data);
        
    } catch (error) {
        console.error('❌ 测试失败:', error.message);
    }
}

// 运行快速测试
// quickTest();
```

## 🔗 相关链接

- **📖 在线文档**: http://localhost:8000/docs (开发环境)
- **📋 完整接口文档**: [API接口文档.md](./API接口文档.md)
- **📚 项目说明**: [README.md](./README.md)

---

**📝 文档状态**: ✅ 已完成核心功能实现  
**🔄 最后同步**: 2024年12月 - 密码验证加强版本 