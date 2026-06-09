# SmartCourse - 基于大语言模型的课堂互动教学系统

## 项目简介

SmartCourse 是一套面向高校课堂的互动教学系统，支持教师端可视化编排作业、AI 智能出题、学生端在线作答、大模型自动批改与学情分析报告生成。

## 技术栈

后端：FastAPI / SQLAlchemy / MySQL / ChromaDB  
前端：Vue 3 + uni-app

## 项目结构

```
SmartCourse/
├── backend/
│   ├── main.py
│   ├── routers/        # API 路由
│   ├── models/         # 数据库模型
│   ├── schemas/        # 数据校验
│   ├── services/       # 业务逻辑
│   ├── core/rag/       # RAG 引擎
│   ├── utils/          # 工具
│   └── setting/        # 配置
├── frontend/
│   ├── pages/
│   ├── components/
│   └── utils/
├── tools/              # 压测工具
└── test/
```

## 环境要求

- Python 3.12+
- MySQL 8.0
- Node.js 18+

## 快速开始

### 1. 克隆项目

```bash
git clone git@github.com:Zhang-10003/SmartCourse.git
cd SmartCourse
```

### 2. 配置数据库

```sql
CREATE DATABASE smart_course_db CHARACTER SET utf8mb4;
```

### 3. 启动后端

```bash
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

首次启动自动创建数据库表。

### 4. 配置前端

修改 `frontend/utils/config.js` 中的 `baseUrl` 为后端 IP。  
使用 HBuilder X 打开 `frontend/` 目录运行。

## 核心功能

可视化作业编排、AI 智能出题、分享链接发布、在线作答、自动批改、学情分析报告、实时 SSE 推送

## 支持题型

单选题、多选题、判断题、填空题、简答题、匹配题、代码填空
