# TodoApp01 技术架构文档

## 一、项目概述

本项目是一个现代化的待办事项管理应用，采用前后端分离架构，前端使用React，后端使用FastAPI，数据库使用SQLite，实现完整的CRUD操作和用户交互功能。

## 二、技术栈

### 前端技术栈

- **框架**: React 18
- **语言**: JavaScript
- **样式**: CSS3 (原生样式，符合设计要求)
- **HTTP客户端**: Axios
- **构建工具**: Vite

### 后端技术栈

- **框架**: FastAPI
- **语言**: Python 3.9+
- **数据库**: SQLite
- **ORM**: SQLAlchemy
- **数据验证**: Pydantic
- **跨域处理**: FastAPI-CORS

## 三、系统架构

```
TodoApp01/
├── backend/                 # 后端目录
│   ├── main.py             # 主应用入口
│   ├── database.py         # 数据库配置
│   ├── models.py           # 数据模型
│   ├── schemas.py          # Pydantic模型
│   ├── crud.py             # 数据库操作
│   ├── requirements.txt    # Python依赖
│   └── todo.db             # SQLite数据库文件
├── front/                  # 前端目录
│   ├── src/
│   │   ├── App.jsx        # 主应用组件
│   │   ├── main.jsx       # 入口文件
│   │   └── App.css        # 样式文件
│   ├── package.json       # Node.js依赖
│   └── vite.config.js     # Vite配置
├── req.md                 # 需求文档
└── TECH_ARCHITECTURE.md    # 本技术架构文档
```

## 四、数据库设计

### 数据表结构

#### 待办事项表 (todos)

```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_todos_completed ON todos(completed);
CREATE INDEX idx_todos_created_at ON todos(created_at);
```

### 字段说明

| 字段名     | 类型      | 说明                |
| ---------- | --------- | ------------------- |
| id         | INTEGER   | 主键，自增          |
| title      | TEXT      | 待办事项标题，必填  |
| completed  | BOOLEAN   | 是否完成，默认false |
| created_at | TIMESTAMP | 创建时间            |
| updated_at | TIMESTAMP | 更新时间            |

## 五、API接口说明

### 基础URL

`http://localhost:8000`

### 所有接口

#### 1. 获取所有待办事项

```
GET /api/todos/
```

查询参数：

- `status`: 可选，过滤状态，可选值：all(默认), pending, completed

响应示例：

```json
{
  "data": [
    {
      "id": 1,
      "title": "学习React",
      "completed": false,
      "created_at": "2026-06-03T10:00:00",
      "updated_at": "2026-06-03T10:00:00"
    }
  ]
}
```

#### 2. 创建新的待办事项

```
POST /api/todos/
```

请求体：

```json
{
  "title": "学习FastAPI"
}
```

响应示例：

```json
{
  "id": 2,
  "title": "学习FastAPI",
  "completed": false,
  "created_at": "2026-06-03T10:30:00",
  "updated_at": "2026-06-03T10:30:00"
}
```

#### 3. 更新待办事项

```
PUT /api/todos/{todo_id}
```

请求体：

```json
{
  "title": "学习FastAPI和React",
  "completed": true
}
```

#### 4. 删除待办事项

```
DELETE /api/todos/{todo_id}
```

#### 5. 批量清除已完成的待办事项

```
DELETE /api/todos/clear-completed
```

#### 6. 清除所有待办事项

```
DELETE /api/todos/clear-all
```

### HTTP状态码

- 200: 成功
- 201: 创建成功
- 404: 资源不存在
- 400: 请求参数错误
- 500: 服务器内部错误

## 六、前端功能说明

### 核心功能

1. **添加待办事项**: 用户输入内容后点击添加按钮，将新任务添加到列表
2. **标记完成**: 点击"完成"按钮，任务文字添加删除线，表示已完成
3. **删除事项**: 点击"删除"按钮，从列表中移除该任务
4. **筛选功能**:
   - 全部：显示所有任务
   - 未完成：只显示未完成的任务
   - 已完成：只显示已完成的任务
5. **批量操作**:
   - 清除已完成：删除所有已完成的任务
   - 清除全部：删除所有任务

### 样式要求

- 主体居中显示，最大宽度800px
- 输入框和按钮样式美观
- 列表项之间有间距
- 鼠标悬停时有视觉反馈效果
- 已完成项添加'completed'类，文字划掉

## 七、部署与启动

### 后端启动

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 前端启动

```bash
cd front
npm install
npm run dev
```

## 八、测试说明

### 后端测试

FastAPI自带自动文档，启动后访问：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 接口测试流程

1. 创建几个测试待办事项
2. 测试获取不同状态的列表
3. 测试更新任务完成状态
4. 测试删除单个任务
5. 测试批量清除功能

## 九、开发计划

1. 先完成后端所有接口开发
2. 进行接口测试，确保所有功能正常
3. 开发前端页面和交互功能
4. 前后端联调，确保数据流转正常
5. 整体测试和优化
