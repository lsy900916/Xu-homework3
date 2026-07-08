# TodoApp 后端测试指导文档

## 目录结构

- `backend/tests/`
  - `conftest.py` - 测试环境配置
  - `test_crud.py` - CRUD 逻辑单元测试
  - `test_main.py` - API 路由集成测试
- `backend/test_todo.db` - 测试期间生成的 SQLite 数据库文件（测试完成后会自动删除）
- `backend/pytest_report.txt` - 最新一次测试执行的结果报告

## 测试前准备

1. 进入后端目录：
   ```bash
   cd backend
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 运行测试

在 `backend` 目录下，执行：

```bash
python -m pytest -q
```

如果需要详细输出，可以执行：

```bash
python -m pytest -vv
```

## 测试报告位置

- 执行测试后，结果会写入：
  - `backend/pytest_report.txt`
- 如果需要手动查看：
  - 打开 `backend/pytest_report.txt`

## 测试流程说明

1. `backend/tests/conftest.py`
   - 通过 `TestClient` 启动 FastAPI 应用
   - 使用测试数据库 `backend/tests/test_todo.db`
   - 覆盖 `get_db` 依赖，使测试使用同一数据库连接
   - 测试结束后删除临时数据库文件

2. `backend/tests/test_crud.py`
   - 测试创建待办事项
   - 测试按 `status` 过滤查询
   - 测试更新待办事项并处理不存在的记录
   - 测试删除单条记录
   - 测试清除已完成记录和清除所有记录

3. `backend/tests/test_main.py`
   - 测试根路由 `/`
   - 测试创建待办事项 API
   - 测试空标题校验
   - 测试更新和删除 API
   - 测试清除已完成和清除所有 API

## 测试结果说明

- 通过：`10 passed`
- 如果失败，请检查：
  - `backend/pytest_report.txt`
  - `backend/tests/conftest.py` 中数据库初始化逻辑
  - `backend/main.py` 中 API 路由顺序和返回值

## 备注

- 当前测试使用 `pytest` 和 `fastapi.testclient`
- 临时测试数据库文件仅在测试会话中生成，测试结束后会被删除
