from sqlalchemy.orm import Session
from models import Todo
from schemas import TodoCreate, TodoUpdate
from typing import List, Optional

def get_todos(db: Session, status: Optional[str] = "all") -> List[Todo]:
    """获取待办事项列表"""
    query = db.query(Todo)
    if status == "pending":
        query = query.filter(Todo.completed == False)
    elif status == "completed":
        query = query.filter(Todo.completed == True)
    return query.order_by(Todo.created_at.desc()).all()

def create_todo(db: Session, todo: TodoCreate) -> Todo:
    """创建新的待办事项"""
    db_todo = Todo(title=todo.title, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate) -> Optional[Todo]:
    """更新待办事项"""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        return None
    
    update_data = todo_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int) -> bool:
    """删除单个待办事项"""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        return False
    db.delete(db_todo)
    db.commit()
    return True

def clear_completed_todos(db: Session) -> int:
    """清除所有已完成的待办事项，返回删除的数量"""
    deleted = db.query(Todo).filter(Todo.completed == True).delete()
    db.commit()
    return deleted

def clear_all_todos(db: Session) -> int:
    """清除所有待办事项，返回删除的数量"""
    deleted = db.query(Todo).delete()
    db.commit()
    return deleted