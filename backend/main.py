from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional

from database import SessionLocal, init_db
from schemas import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse, SuccessResponse
import crud

# 初始化数据库
init_db()

# 创建FastAPI应用
app = FastAPI(title="Todo App API", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库会话依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API路由
@app.get("/api/todos/", response_model=TodoListResponse, summary="获取待办事项列表")
def read_todos(status: Optional[str] = "all", db: Session = Depends(get_db)):
    """
    获取待办事项列表，支持按状态筛选：
    - status=all: 返回所有待办事项（默认）
    - status=pending: 只返回未完成的待办事项
    - status=completed: 只返回已完成的待办事项
    """
    todos = crud.get_todos(db, status)
    return {"data": todos, "total": len(todos)}

@app.post("/api/todos/", response_model=TodoResponse, status_code=201, summary="创建新的待办事项")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """
    创建一个新的待办事项
    """
    if not todo.title.strip():
        raise HTTPException(status_code=400, detail="待办事项标题不能为空")
    return crud.create_todo(db, todo)

@app.put("/api/todos/{todo_id}", response_model=TodoResponse, summary="更新待办事项")
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    """
    根据ID更新待办事项的信息
    """
    db_todo = crud.update_todo(db, todo_id, todo_update)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="待办事项不存在")
    return db_todo

@app.delete("/api/todos/clear-completed", response_model=SuccessResponse, summary="清除所有已完成的待办事项")
def clear_completed_todos(db: Session = Depends(get_db)):
    """
    删除所有已完成的待办事项，返回删除的数量
    """
    deleted_count = crud.clear_completed_todos(db)
    return {"message": f"成功清除{deleted_count}个已完成的待办事项", "deleted_count": deleted_count}

@app.delete("/api/todos/clear-all", response_model=SuccessResponse, summary="清除所有待办事项")
def clear_all_todos(db: Session = Depends(get_db)):
    """
    删除所有待办事项，返回删除的数量
    """
    deleted_count = crud.clear_all_todos(db)
    return {"message": f"成功清除所有{deleted_count}个待办事项", "deleted_count": deleted_count}

@app.delete("/api/todos/{todo_id}", summary="删除待办事项")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    根据ID删除单个待办事项
    """
    success = crud.delete_todo(db, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="待办事项不存在")
    return {"message": "删除成功"}

# 根路由
@app.get("/")
def root():
    return {"message": "Welcome to Todo App API", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)