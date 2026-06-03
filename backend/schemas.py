from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Todo基础模式
class TodoBase(BaseModel):
    title: str
    completed: Optional[bool] = False

# 创建Todo时的请求模式
class TodoCreate(TodoBase):
    pass

# 更新Todo时的请求模式
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

# 返回给客户端的Todo模式
class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 列表响应模式
class TodoListResponse(BaseModel):
    data: List[TodoResponse]
    total: int

# 操作结果响应
class SuccessResponse(BaseModel):
    message: str
    deleted_count: int