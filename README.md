# minco 后端服务

基于FastAPI的媒体文件处理服务。

## 快速启动

1. 创建虚拟环境
```bash
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
# 或
venv\Scripts\activate  # Windows
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 启动服务
```bash
uvicorn main:app --reload
```

## 主要接口

- 登录: POST /auth/login
- 登出: POST /auth/logout
