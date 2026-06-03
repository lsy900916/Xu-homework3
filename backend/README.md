# TodoApp 后端服务

## 项目介绍

这是一个使用FastAPI框架开发的待办事项应用后端服务，提供完整的RESTful API接口，使用SQLite作为数据库。

## 功能特性

- ✅ 创建待办事项
- ✅ 获取待办事项列表（支持按状态筛选）
- ✅ 更新待办事项（标记完成/修改标题）
- ✅ 删除单个待办事项
- ✅ 批量清除已完成的待办事项
- ✅ 清除所有待办事项
- ✅ 自动API文档
- ✅ 跨域支持

## 环境要求

- Python 3.9+
- pip

## 安装与启动

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动服务

```bash
uvicorn main:app --reload
```

服务启动后，访问以下地址：

- API根地址: http://localhost:8000
- Swagger UI文档: http://localhost:8000/docs
- ReDoc文档: http://localhost:8000/redoc

## API接口说明

### 获取待办事项列表

```
GET /api/todos/
```

查询参数：

- `status`: 可选，默认all
  - all: 全部
  - pending: 未完成
  - completed: 已完成

### 创建待办事项

```
POST /api/todos/
Content-Type: application/json

{
  "title": "学习FastAPI"
}
```

### 更新待办事项

```
PUT /api/todos/{todo_id}
Content-Type: application/json

{
  "title": "更新后的标题",
  "completed": true
}
```

### 删除待办事项

```
DELETE /api/todos/{todo_id}
```

### 清除已完成的待办事项

```
DELETE /api/todos/clear-completed
```

### 清除所有待办事项

```
DELETE /api/todos/clear-all
```

## 数据库结构

应用会自动创建`todo.db` SQLite数据库文件，包含一张`todos`表：

| 字段       | 类型     | 说明         |
| ---------- | -------- | ------------ |
| id         | INTEGER  | 主键，自增   |
| title      | TEXT     | 待办事项标题 |
| completed  | BOOLEAN  | 是否完成     |
| created_at | DATETIME | 创建时间     |
| updated_at | DATETIME | 更新时间     |

## 开发说明

- 数据库使用SQLAlchemy ORM管理
- 数据验证使用Pydantic
- 所有的数据库操作都封装在`crud.py`中
- 启动时会自动初始化数据库表结构

## 测试方法

启动服务后，访问 http://localhost:8000/docs 可以在Swagger UI中直接测试所有接口。
