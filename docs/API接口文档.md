# API 接口文档

## 📋 接口总览清单

### 🎯 优先级统计

| 优先级 | 接口数量 | 开发状态 | 说明 |
|--------|----------|----------|------|
| P0 核心 | 10个 | 待开发 | MVP必需功能 |
| P1 重要 | 13个 | 待开发 | 重要业务功能 |
| P2 增强 | 6个 | 待开发 | 增强体验功能 |
| **总计** | **29个** | **-** | **完整产品功能** |

## 📊 完整接口清单

| 序号 | 优先级 | 接口名称 | 方法 | 路径 | 功能描述 | 前端页面 |
|------|--------|----------|------|------|----------|----------|
| **基础事项管理** |
| 1 | P0 | 获取事项列表 | GET | /items | 获取用户事项，支持筛选 | 时间轴、项目 |
| 2 | P0 | 创建事项 | POST | /items | 快速/详细添加事项 | 全局浮层 |
| 3 | P0 | 获取单个事项 | GET | /items/{itemId} | 获取单个事项详情 | - |
| 4 | P0 | 更新事项 | PUT | /items/{itemId} | 编辑事项信息 | 事项详情 |
| 7 | P0 | 删除事项 | DELETE | /items/{itemId} | 删除事项 | 时间轴滑动 |
| 8 | P2 | 批量操作事项 | POST | /items/batch | 批量完成/删除/移动 | 时间轴页 |
| 9 | P1 | 获取推荐事项列表 | GET | /items/recommendations | 展示推荐当前最需要处理的事项 | - |
| **项目管理** |
| 7 | P1 | 获取项目列表 | GET | /projects | 按分类获取项目 | 项目页 |
| 8 | P1 | 创建项目 | POST | /projects | 手动创建项目 | 项目页浮层 |
| 9 | P1 | 获取项目详情 | GET | /projects/{id} | 项目详情+统计 | 项目详情页 |
| 10 | P1 | 更新项目 | PUT | /projects/{id} | 编辑项目信息 | 项目详情页 |
| **AI智能功能** |
| 11 | P0 | 智能推荐 | POST | /ai/recommendations | 首页决策区推荐算法 | 首页决策区 |
| 12 | P1 | 项目自动归集 | POST | /ai/project-grouping | AI自动分类事项到项目 | 项目详情页 |
| 13 | P1 | AI助手对话 | POST | /ai/chat | 智能对话+快速回复 | 全局AI浮层 |
| 14 | P1 | 事项智能分析 | POST | /ai/task-analysis | 智能估时+分类+子任务 | 添加事项浮层 |
| 15 | P1 | 任务拆解 | POST | /ai/task-breakdown | 复杂任务拆解为子任务 | 事项详情页 |
| **专注与规划** |
| 16 | P0 | 开始专注 | POST | /focus/start | 开启专注模式 | 专注页面 |
| 17 | P0 | 结束专注 | POST | /focus/{id}/end | 结束专注+记录 | 专注页面 |
| 18 | P1 | 每日规划 | POST | /daily/plan | AI生成每日计划 | 首页规划区 |
| 19 | P1 | 每日回顾 | POST | /daily/review | 每日完成情况回顾 | 首页回顾区 |
| **用户认证** |
| 20 | P0 | 用户登录 | POST | /auth/login | 用户认证 | 登录页 |
| 21 | P0 | 获取用户信息 | GET | /user/profile | 用户基础信息 | 我的页面 |
| 22 | P2 | 更新用户设置 | PUT | /user/settings | 个人偏好设置 | 我的页面 |
| **统计分析** |
| 23 | P2 | 获取统计数据 | GET | /statistics | 完成率、趋势分析 | 我的页面 |
| **系统功能** |
| 24 | P2 | 数据导出 | GET | /export/data | 导出用户数据 | 我的页面 |
| 25 | P2 | 消息通知 | GET | /notifications | 系统消息推送 | 全局 |
| 26 | P2 | 数据同步 | POST | /sync | 多设备数据同步 | 后台 |

## 🎯 按前端页面分组

| 页面 | 核心接口 | 接口数量 | 开发优先级 |
|------|----------|----------|------------|
| 首页决策区 | 智能推荐、完成事项、每日规划/回顾 | 4个 | P0+P1 |
| 时间轴页 | 获取事项列表、完成事项、删除事项、批量操作 | 4个 | P0+P2 |
| 项目页 | 项目CRUD、项目详情、自动归集 | 4个 | P1 |
| 我的页面 | 用户信息、设置、统计、导出 | 4个 | P0+P2 |
| 全局功能 | 事项CRUD、AI对话、专注模式、通知 | 10个 | P0+P1+P2 |

## 🤖 AI功能接口分类

| AI功能 | 接口名称 | 现有资源 | 开发方式 | 优先级 |
|--------|----------|----------|----------|--------|
| 智能推荐 | /ai/recommendations | ✅ 现有agent | 全新算法 | P0 |
| 项目归集 | /ai/project-grouping | ✅ 现有agent | 全新算法 | P1 |
| 意图识别 | /ai/chat | ✅ 现有agent | 包装调用 | P1 |
| 事项分析 | /ai/task-analysis | ✅ 现有agent | 包装调用 | P1 |
| 任务拆解 | /ai/task-breakdown | ✅ 现有agent | 包装调用 | P1 |
| 情绪支持 | /ai/chat (模式) | ✅ 现有agent | 包装调用 | P1 |

## 🗂️ 数据模型定义

### 事项 (Task)

```json
{
  "id": "string",
  "title": "string",
  "description": "string (nullable)",
  "emoji": "string (nullable)",
  "category_id": "integer (1:生活, 2:健康, 3:工作, 4:学习, 5:放松, 6:探索)",
  "project_id": "string (nullable)",
  "start_time": "string (date-time ISO 8601, nullable)",
  "end_time": "string (date-time ISO 8601, nullable)",
  "estimated_duration": "integer (minutes, nullable)",
  "time_slot_id": "integer (1:上午, 2:中午, 3:下午, 4:晚上, 5:随时, nullable)",
  "priority": "integer (1-5, 5为最高)",
  "status_id": "integer (1:pending, 2:in_progress, 3:completed, 4:cancelled)",
  "is_overdue": "boolean",
  "sub_tasks": ["string (nullable)"],
  "created_at": "string (date-time ISO 8601, e.g. 2024-05-24T09:00:00Z)",
  "updated_at": "string (date-time ISO 8601)",
  "completed_at": "string (date-time ISO 8601, nullable)"
}
```

### 项目 (Project)

```json
{
  "id": "string",
  "title": "string",
  "description": "string (nullable)",
  "category_id": "integer (1:生活, 2:健康, 3:工作, 4:学习, 5:放松, 6:探索)",
  "emoji": "string (nullable)",
  "color": "string (hex color, nullable)",
  "progress": "number (float, 0.0-1.0, nullable)",
  "start_date": "string (date ISO 8601, nullable)",
  "end_date": "string (date ISO 8601, nullable)",
  "notes": "string (nullable)",
  "task_count": "integer (15)",
  "completed_task_count": "integer (10)",
  "created_at": "string (date-time ISO 8601)",
  "updated_at": "string (date-time ISO 8601)"
}
```

### 用户 (User)

```json
{
  "id": "string",
  "username": "string",
  "email": "string (email format, for login)",
  "full_name": "string (nullable, for registration)",
  "avatar": "string (url, nullable)",
  "personal_tags": ["string (nullable)"] (["MBTI-INFP", "夜猫子"]),
  "long_term_goals": ["string (nullable)"] (["身体健康", "职业发展"]),
  "recent_focus": ["string (nullable)"] (["写论文", "学习编程"]),
  "daily_plan_time": "string (time, HH:MM, e.g.08:00, nullable)",
  "daily_review_time": "string (time, HH:MM, e.g.22:00, nullable)",
  "timezone": "string (e.g., Asia/Shanghai, nullable)",
  "created_at": "string (date-time ISO 8601)"
}
```

### 专注会话 (FocusSession)

```json
{
  "id": "string",
  "task_id": "string",
  "start_time": "string (date-time ISO 8601)",
  "end_time": "string (date-time ISO 8601, nullable)",
  "planned_duration": "integer (seconds, e.g. 1800)",
  "actual_duration": "integer (seconds, e.g. 1500, nullable)",
  "mode_id": "integer (1:pomodoro, 2:free)",
  "completed": "boolean",
  "interruptions": "integer (nullable)"
}
```

## 🔗 基础配置

- **开发环境URL**: `http://localhost:8000/api/v1`
- **生产环境URL**: `https://api.minco.app/api/v1`
- **通用请求头**: 除特殊说明外，以下所有需要认证的接口均需在请求头中包含:
  ```
  Authorization: Bearer {access_token}
  ```
- **认证方式**: Bearer Token (JWT)
- **数据格式**: JSON
- **字符编码**: UTF-8
- **超时设置**: API响应 < 500ms，AI接口 < 2s

## 📊 统一响应格式

所有接口均返回统一的响应格式：

```json
{
  "code": 0,           // 响应码 (0:成功, 非0:错误)
  "message": "success", // 响应消息
  "data": {}           // 响应数据 (具体格式见各接口说明)
}
```

## 📱 详细接口文档

### 基础事项管理

#### 1.1 创建新事项

**功能说明**: 对应产品文档中的"事项添加"功能，允许用户创建新的事项。

- **请求方式**: `POST`
- **请求地址**: `/items`
- **请求头**:
  ```
  Authorization: Bearer {token}
  Content-Type: application/json
  ```

**请求体**:
```json
{
  "title": "string", // 事项标题 (必填)
  "description": "string", // 事项详细描述 (可选)
  "emoji": "string", // 事项关联的表情符号 (可选)
  "category_id": "integer", // 事项分类ID (必填, 映射关系: 1:生活, 2:健康, 3:工作, 4:学习, 5:放松, 6:探索)
  "project_id": "string", // 所属项目的ID (可选)
  "start_time": "string", // 开始时间 (ISO 8601 格式, YYYY-MM-DDTHH:mm:ssZ, 可选)
  "end_time": "string", // 结束时间 (ISO 8601 格式, YYYY-MM-DDTHH:mm:ssZ, 可选)
  "estimated_duration": "integer", // 预估用时（分钟, 可选)
  "time_slot_id": "integer", // 时间段ID (可选, 映射关系: 1:上午, 2:中午, 3:下午, 4:晚上, 5:随时)
  "priority": "integer", // 优先级 (必填, 1-5, 具体含义需业务定义，例如5为最高)
  "status_id": "integer", // 状态ID (可选, 默认为1:待处理, 映射关系: 1:pending, 2:in_progress, 3:completed, 4:cancelled)
  "sub_tasks": ["string"] // 子任务描述列表 (可选)
}
```

**响应体** (HTTP 201 Created):
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "string", // 新创建事项的唯一标识符
    "title": "string",
    "description": "string",
    "emoji": "string",
    "category_id": "integer",
    "project_id": "string",
    "start_time": "string",
    "end_time": "string",
    "estimated_duration": "integer",
    "time_slot_id": "integer",
    "priority": "integer",
    "status_id": "integer",
    "is_overdue": "boolean",
    "sub_tasks": ["string"],
    "created_at": "string", // 创建时间 (ISO 8601)
    "updated_at": "string"  // 更新时间 (ISO 8601)
  }
}
```

#### 1.2 获取事项列表

**功能说明**: 获取用户的事项列表，支持多种筛选条件，用于时间轴、项目内事项列表等场景。

- **请求方式**: `GET`
- **请求地址**: `/items`
- **请求头**:
  ```
  Authorization: Bearer {token}
  ```

**查询参数** (均为可选):
- `date`: string (格式 YYYY-MM-DD, 用于筛选特定日期范围内的事项)
- `project_id`: string (筛选特定项目下的事项)
- `category_id`: integer (筛选特定分类的事项)
- `status_id`: integer (筛选特定状态的事项)
- `priority`: integer (筛选特定优先级的事项)
- `is_completed`: boolean (true 表示已完成事项，false 表示未完成事项)
- `time_slot_id`: integer (筛选特定时间段的事项)
- `sort_by`: string (排序字段，如 created_at, start_time, priority)
- `order`: string (asc 或 desc，排序顺序)
- `page`: integer (页码，用于分页，默认1)
- `limit`: integer (每页数量，用于分页，默认20)

**响应体** (HTTP 200 OK):
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "string",
        "title": "string",
        "category_id": "integer",
        "priority": "integer",
        "status_id": "integer",
        "start_time": "string",
        "created_at": "string",
        "updated_at": "string"
      }
    ],
    "pagination": {
      "total_items": "integer", // 总事项数
      "total_pages": "integer", // 总页数
      "current_page": "integer", // 当前页码
      "limit": "integer" // 每页数量
    }
  }
}
```

#### 1.3 获取单个事项详情

**功能说明**: 获取指定ID事项的详细信息，对应产品文档中"点击事项卡片查看事项详情"。

- **请求方式**: `GET`
- **请求地址**: `/items/{itemId}`
- **请求头**:
  ```
  Authorization: Bearer {token}
  ```

**路径参数**:
- `itemId` (string): 要获取详情的事项的唯一ID

**响应体** (HTTP 200 OK):
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "string",
    "title": "string",
    "description": "string",
    "emoji": "string",
    "category_id": "integer",
    "project_id": "string",
    "start_time": "string",
    "end_time": "string",
    "estimated_duration": "integer",
    "time_slot_id": "integer",
    "priority": "integer",
    "status_id": "integer",
    "is_overdue": "boolean",
    "sub_tasks": ["string"],
    "created_at": "string",
    "updated_at": "string",
    "completed_at": "string"
  }
}
```

#### 1.4 更新事项信息

**功能说明**: 修改现有事项的详细信息。

- **请求方式**: `PUT`
- **请求地址**: `/items/{itemId}`
- **请求头**:
  ```
  Authorization: Bearer {token}
  Content-Type: application/json
  ```

**路径参数**:
- `itemId` (string): 要更新的事项的唯一ID

**请求体**:
```json
{
  "title": "string", // (可选)
  "description": "string", // (可选)
  "emoji": "string", // (可选)
  "category_id": "integer", // (可选)
  "project_id": "string", // (可选)
  "start_time": "string", // (可选, ISO 8601)
  "end_time": "string", // (可选, ISO 8601)
  "estimated_duration": "integer", // (可选)
  "time_slot_id": "integer", // (可选)
  "priority": "integer", // (可选, 1-5)
  "status_id": "integer", // (可选)
  "sub_tasks": ["string"] // (可选, 会替换整个子任务列表)
}
```

**响应体** (HTTP 200 OK):
```json
{
  "code": 0,
  "message": "success", 
  "data": {
    "id": "string",
    "title": "string",
    "description": "string",
    "emoji": "string",
    "category_id": "integer",
    "project_id": "string",
    "start_time": "string",
    "end_time": "string",
    "estimated_duration": "integer",
    "time_slot_id": "integer",
    "priority": "integer",
    "status_id": "integer",
    "is_overdue": "boolean",
    "sub_tasks": ["string"],
    "created_at": "string",
    "updated_at": "string" // 更新时间会改变
  }
}
```

#### 1.7 删除事项

**功能说明**: 删除一个事项，对应产品文档中时间轴的左滑删除功能。

- **请求方式**: `DELETE`
- **请求地址**: `/items/{itemId}`
- **请求头**:
  ```
  Authorization: Bearer {token}
  ```

**路径参数**:
- `itemId` (string): 要删除的事项的唯一ID

**响应体** (HTTP 204 No Content): 成功删除通常无响应体

#### 1.8 批量操作事项

**功能说明**: 批量处理多个事项，如批量删除、批量标记完成、批量移动等。

- **请求方式**: `POST`
- **请求地址**: `/items/batch`
- **请求头**:
  ```
  Authorization: Bearer {token}
  Content-Type: application/json
  ```

**请求体**:
```json
{
  "action": "string", // 操作类型 (例如 "delete", "complete", "move_to_project", "change_status")
  "item_ids": ["string"], // 要操作的事项ID列表 (必填)
  "payload": {
    "target_project_id": "string", // (可选, 用于 action="move_to_project")
    "new_status_id": "integer"    // (可选, 用于 action="change_status")
  }
}
```

**响应体** (HTTP 200 OK):
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "action": "string", // 执行的操作
    "results": [
      {
        "item_id": "string",
        "success": "boolean",
        "message": "string" // (可选, 失败时的原因)
      }
    ],
    "summary": {
      "total_processed": "integer",
      "total_succeeded": "integer",
      "total_failed": "integer"
    }
  }
}
```

#### 1.9 获取推荐事项列表

**功能说明**: 为首页"决策区"获取AI推荐的当前最需要处理的事项列表。

- **请求方式**: `GET`
- **请求地址**: `/items/recommendations`
- **请求头**:
  ```
  Authorization: Bearer {token}
  ```

**查询参数** (可选, 用于给AI更多上下文):
- `count`: integer (期望推荐的数量，例如 3-5，默认为3)
- `current_mood`: string (用户当前心情，例如 "focused", "tired", "energetic")
- `available_time_minutes`: integer (用户当前可用时长，单位分钟)

**响应体** (HTTP 200 OK):
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "recommendations": [
      {
        "item": {
          "id": "string",
          "title": "string",
          "category_id": "integer"
        },
        "reason": "string", // AI推荐该事项的理由 (例如 "现在是上午，精力充沛，适合处理重要工作")
        "confidence_score": "number" // (可选, AI对推荐的置信度)
      }
    ],
    "message": "string" // (可选, 整体推荐的提示信息)
  }
}
```

### 2. 项目管理

#### 2.1 [P1] 获取项目列表
- **请求方式**: `GET`
- **请求地址**: `/projects`

**查询参数**:
- `category`: 工作 (可选)
- `include_tasks`: true (可选，是否包含事项)

#### 2.2 [P1] 创建项目
- **请求方式**: `POST`
- **请求地址**: `/projects`

**请求体**:
```json
{
  "title": "健身计划",
  "description": "2024年健身目标",
  "category": "健康",
  "emoji": "💪",
  "color": "#FF5733"
}
```

#### 2.3 [P1] 获取项目详情
- **请求方式**: `GET`
- **请求地址**: `/projects/{project_id}`

**响应**:
```json
{
  "code": 200,
  "data": {
    "project": "Project",
    "tasks": ["Task"],
    "statistics": {
      "total_tasks": 15,
      "completed_tasks": 10,
      "overdue_tasks": 2,
      "progress_percentage": 66.7
    }
  }
}
```

#### 2.4 [P1] 更新项目
- **请求方式**: `PUT`
- **请求地址**: `/projects/{project_id}`

### 3. AI智能功能

#### 3.1 [P0] 智能推荐
- **请求方式**: `POST`
- **请求地址**: `/ai/recommendations`

**请求体**:
```json
{
  "user_context": {
    "current_time": "2024-05-24T09:00:00Z",
    "mood": "focused|tired|energetic",
    "available_time": 120
  },
  "count": 3
}
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "recommendations": [
      {
        "task": "Task",
        "reason": "现在是上午，精力充沛，适合处理重要工作",
        "confidence": 0.85
      }
    ],
    "total_available": 12
  }
}
```

#### 3.2 [P1] 项目自动归集
- **请求方式**: `POST`
- **请求地址**: `/ai/project-grouping`

**请求体**:
```json
{
  "tasks": ["task_id1", "task_id2"],
  "user_goals": ["身体健康", "职业发展"]
}
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "suggested_projects": [
      {
        "title": "健身计划",
        "category": "健康",
        "tasks": ["task_id1"],
        "confidence": 0.9
      }
    ],
    "ungrouped_tasks": ["task_id2"]
  }
}
```

#### 3.3 [P1] AI助手对话
- **请求方式**: `POST`
- **请求地址**: `/ai/chat`

**请求体**:
```json
{
  "message": "我感觉有点卡住了",
  "context": {
    "recent_tasks": ["task_id1", "task_id2"],
    "current_projects": ["project_id1"]
  }
}
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "reply": "我理解你的感受。要不要试试把大任务拆解成小步骤？",
    "suggested_actions": [
      {
        "type": "task_breakdown",
        "task_id": "task_id1",
        "label": "拆解这个任务"
      }
    ],
    "quick_replies": [
      "看看这周有什么事项",
      "需要一点动力"
    ]
  }
}
```

#### 3.4 [P1] 事项智能分析
- **请求方式**: `POST`
- **请求地址**: `/ai/task-analysis`

**请求体**:
```json
{
  "task_description": "写产品需求文档"
}
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "suggested_category": "工作",
    "estimated_duration": 120,
    "suggested_emoji": "📝",
    "sub_tasks": [
      "整理功能清单",
      "绘制用户流程",
      "编写接口文档"
    ],
    "best_time_slot": "上午"
  }
}
```

#### 3.5 [P1] 任务拆解
- **请求方式**: `POST`
- **请求地址**: `/ai/task-breakdown`

**请求体**:
```json
{
  "task_id": "string",
  "complexity_level": "simple|medium|complex"
}
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "parent_task": "Task",
    "sub_tasks": [
      {
        "title": "整理功能清单",
        "estimated_duration": 30,
        "order": 1
      }
    ],
    "estimated_total_time": 120
  }
}
```

### 4. 专注与规划

#### 4.1 [P0] 开始专注
- **请求方式**: `POST`
- **请求地址**: `/focus/start`

**请求体**:
```json
{
  "task_id": "string",
  "duration": 1800,
  "mode": "pomodoro|free"
}
```

**响应体** (HTTP 200 OK):
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "session_id": "string",
    "start_time": "2024-05-24T09:00:00Z",
    "end_time": "2024-05-24T09:30:00Z",
    "task": {
      "id": "string",
      "title": "string",
      "emoji": "string",
      "category_id": "integer",
      "priority": "integer",
      "status_id": "integer",
      "created_at": "string",
      "updated_at": "string"
    }
  }
}
```
#### 4.2 [P0] 结束专注
- **请求方式**: `POST`
- **请求地址**: `/focus/{session_id}/end`

**请求体**:
```json
{
  "actual_duration": 1800,
  "completed": true,
  "interruptions": 2
}
```

#### 4.3 [P1] 每日规划
- **请求方式**: `POST`
- **请求地址**: `/daily/plan`

**请求体**:
```json
{
  "date": "2024-05-24",
  "available_time": 480,
  "priorities": ["project_id1", "urgent_tasks"]
}
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "top_three": ["Task"],
    "schedule": [
      {
        "time_slot": "上午",
        "tasks": ["Task"]
      }
    ],
    "suggestions": "建议上午处理重要工作，下午安排轻松任务"
  }
}
```

#### 4.4 [P1] 每日回顾
- **请求方式**: `POST`
- **请求地址**: `/daily/review`

**请求体**:
```json
{
  "date": "2024-05-24"
}
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "completed_tasks": ["Task"],
    "incomplete_tasks": ["Task"],
    "top_three_status": {
      "completed": 2,
      "total": 3
    },
    "suggestions": [
      {
        "task_id": "string",
        "action": "reschedule",
        "suggested_date": "2024-05-25"
      }
    ],
    "encouragement": "今天完成了67%的任务，表现不错！"
  }
}
```

### 5. 系统测试

#### 5.0 [P0] 连接测试

**功能说明**: 测试API服务连接状态，用于前端验证服务可用性

- **请求方式**: `POST`
- **请求地址**: `/test/connect_test`
- **请求头**:
  ```
  Content-Type: application/json
  ```

**请求体**:
```json
{
  "uuid": "string"  // 可选的唯一标识符，用于测试追踪
}
```

**响应体** (HTTP 200 OK):
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "status": "success",
    "message": "Connection successful",
    "uuid": "string"  // 返回请求中的uuid
  }
}
```

### 6. 用户认证

#### 6.0 [P0] 用户注册

**功能说明**: 新用户账户注册，创建用户账户并返回认证信息

- **请求方式**: `POST`
- **请求地址**: `/auth/register`
- **请求头**:
  ```
  Content-Type: application/json
  ```

**请求体**:
```json
{
  "username": "string",        // 用户名 (必填, 3-20字符)
  "email": "string",          // 邮箱 (必填, 用于登录)
  "password": "string",       // 密码 (必填, 8-50字符)
  "full_name": "string",      // 真实姓名 (可选)
  "personal_tags": ["string"], // 个人标签 (可选, 如["MBTI-INFP", "夜猫子"])
  "long_term_goals": ["string"], // 长期目标 (可选, 如["身体健康", "职业发展"])
  "timezone": "string"        // 时区 (可选, 默认"Asia/Shanghai")
}
```

**响应体** (HTTP 201 Created):
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",  // JWT访问令牌
    "token_type": "bearer",          // 令牌类型
    "user": {
      "id": "string",
      "username": "string", 
      "email": "string",
      "full_name": "string",
      "avatar": null,
      "personal_tags": ["string"],
      "long_term_goals": ["string"],
      "recent_focus": [],
      "daily_plan_time": "08:00",    // 默认值
      "daily_review_time": "22:00",  // 默认值
      "timezone": "Asia/Shanghai",
      "created_at": "2024-05-24T09:00:00Z"
    },
    "expires_in": 1800  // token有效期(秒, 30分钟)
  }
}
```

#### 5.1.1 [P1] 检查用户名/邮箱可用性

**功能说明**: 注册前检查用户名或邮箱是否已被使用

- **请求方式**: `GET`
- **请求地址**: `/auth/check-availability`

**查询参数**:
- `username`: string (可选)
- `email`: string (可选)

**响应体** (HTTP 200 OK):
```json
{
  "code": 200,
  "data": {
    "username_available": true,  // 用户名是否可用
    "email_available": false     // 邮箱是否可用
  }
}
```

#### 5.1.2 [P2] 发送邮箱验证码

**功能说明**: 为邮箱注册发送验证码

- **请求方式**: `POST`
- **请求地址**: `/auth/send-verification`

**请求体**:
```json
{
  "email": "string",           // 邮箱地址
  "type": "register"           // 验证类型
}
```

**响应体** (HTTP 200 OK):
```json
{
  "code": 200,
  "message": "验证码已发送",
  "data": {
    "expires_in": 300  // 验证码有效期(秒)
  }
}
```

#### 5.1.3 [P2] 验证邮箱验证码

**功能说明**: 验证邮箱验证码有效性

- **请求方式**: `POST`
- **请求地址**: `/auth/verify-code`

**请求体**:
```json
{
  "email": "string",     // 邮箱地址
  "code": "string",      // 6位验证码
  "type": "register"     // 验证类型
}
```

**响应体** (HTTP 200 OK):
```json
{
  "code": 200,
  "message": "验证成功",
  "data": {
    "verified": true,
    "token": "temp_verify_token"  // 临时验证令牌，用于注册
  }
}
```

#### 5.1 [P0] 用户登录

**功能说明**: 用户登录认证，获取访问令牌

- **请求方式**: `POST`
- **请求地址**: `/auth/login`
- **请求头**:
  ```
  Content-Type: application/json
  ```

**请求体**:
```json
{
  "username": "string",    // 用户名或邮箱 (必填)
  "password": "string",    // 密码 (必填, 8-50字符)
  "remember_me": boolean   // 是否记住登录状态 (可选, 默认false)
}
```

**响应体** (HTTP 200 OK):
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",  // JWT访问令牌
    "token_type": "bearer",          // 令牌类型
    "user_id": "integer",            // 用户ID
    "username": "string"             // 用户名
  }
}
```

**错误响应**:
```json
{
  "code": 400,
  "message": "用户名或密码错误",
  "data": null
}
```

**注意事项**:
1. 注册和登录成功后，客户端应保存 `access_token` 用于后续请求的认证
2. 所有需要认证的接口都应在请求头中携带token: `Authorization: Bearer {access_token}`
3. token有效期为30分钟（1800秒），过期后需要重新登录
4. 注册时会自动设置用户Cookie，支持浏览器自动认证
5. 密码需要6-50字符，建议包含字母、数字和特殊字符

#### 5.2 [P0] 获取用户信息
- **请求方式**: `GET`
- **请求地址**: `/user/profile`

#### 5.3 [P2] 更新用户设置
- **请求方式**: `PUT`
- **请求地址**: `/user/settings`

**请求体**:
```json
{
  "daily_plan_time": "08:00",
  "daily_review_time": "22:00",
  "long_term_goals": ["身体健康"],
  "recent_focus": ["写论文"]
}
```

### 6. 统计分析

#### 6.1 [P2] 获取统计数据
- **请求方式**: `GET`
- **请求地址**: `/statistics`

**查询参数**:
- `period`: day|week|month
- `date`: 2024-05-24

**响应**:
```json
{
  "code": 200,
  "data": {
    "completion_rate": 0.75,
    "total_tasks": 20,
    "completed_tasks": 15,
    "total_focus_time": 7200,
    "category_breakdown": {
      "工作": 8,
      "学习": 4,
      "健康": 3
    },
    "productivity_trend": [0.6, 0.7, 0.75, 0.8]
  }
}
```

### 7. 系统功能

#### 7.1 [P2] 数据导出
- **请求方式**: `GET`
- **请求地址**: `/export/data`

**查询参数**:
- `format`: json|csv
- `date_range`: 30 (天数)

#### 7.2 [P2] 消息通知
- **请求方式**: `GET`
- **请求地址**: `/notifications`

**响应**:
```json
{
  "code": 200,
  "data": {
    "notifications": [
      {
        "id": "string",
        "type": "reminder|achievement|system",
        "title": "专注时间到了",
        "message": "25分钟专注完成，休息一下吧",
        "read": false,
        "created_at": "2024-05-24T09:30:00Z"
      }
    ]
  }
}
```

#### 7.3 [P2] 数据同步
- **请求方式**: `POST`
- **请求地址**: `/sync`

**请求体**:
```json
{
  "device_id": "string",
  "last_sync": "2024-05-24T08:00:00Z",
  "local_changes": [
    {
      "type": "task",
      "action": "create|update|delete",
      "data": "Task"
    }
  ]
}
```

## 📊 错误处理

### 标准错误响应

所有错误都使用统一的响应格式：

```json
{
  "code": 400,              // 业务错误码 (非0表示错误)
  "message": "请求参数错误",   // 错误描述信息
  "data": null              // 错误时data为null
}
```

### HTTP状态码与业务错误码对应

| HTTP状态码 | 业务错误码 | 说明 |
|-----------|----------|------|
| 200 | 0 | 请求成功 |
| 201 | 0 | 创建成功 |
| 400 | 400 | 请求参数错误 |
| 401 | 401 | 未授权/认证失败 |
| 403 | 403 | 禁止访问 |
| 404 | 404 | 资源不存在 |
| 500 | 500 | 服务器内部错误 |

### 常见错误示例

#### 参数错误
```json
{
  "code": 400,
  "message": "标题不能为空",
  "data": null
}
```

#### 认证失败
```json
{
  "code": 401,
  "message": "用户名或密码错误",
  "data": null
}
```

#### 服务器错误
```json
{
  "code": 500,
  "message": "服务器内部错误",
  "data": null
}
```
