import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const API_BASE_URL = "http://localhost:8000/api";

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState("");
  const [filter, setFilter] = useState("all"); // all, pending, completed
  const [loading, setLoading] = useState(false);

  // 获取待办事项列表
  const fetchTodos = async (status = "all") => {
    try {
      const response = await axios.get(`${API_BASE_URL}/todos/`, {
        params: {
          status:
            status === "all"
              ? "all"
              : status === "pending"
                ? "pending"
                : "completed",
        },
      });
      setTodos(response.data.data);
    } catch (error) {
      console.error("获取待办事项失败:", error);
    }
  };

  // 初始加载
  useEffect(() => {
    fetchTodos(filter);
  }, [filter]);

  // 添加待办事项
  const addTodo = async () => {
    if (!newTodo.trim()) return;

    try {
      setLoading(true);
      await axios.post(`${API_BASE_URL}/todos/`, { title: newTodo.trim() });
      setNewTodo("");
      fetchTodos(filter);
    } catch (error) {
      console.error("添加待办事项失败:", error);
    } finally {
      setLoading(false);
    }
  };

  // 标记完成
  const toggleComplete = async (todo) => {
    try {
      await axios.put(`${API_BASE_URL}/todos/${todo.id}`, {
        completed: !todo.completed,
      });
      fetchTodos(filter);
    } catch (error) {
      console.error("更新待办事项失败:", error);
    }
  };

  // 删除待办事项
  const deleteTodo = async (todoId) => {
    try {
      await axios.delete(`${API_BASE_URL}/todos/${todoId}`);
      fetchTodos(filter);
    } catch (error) {
      console.error("删除待办事项失败:", error);
    }
  };

  // 清除已完成
  const clearCompleted = async () => {
    try {
      await axios.delete(`${API_BASE_URL}/todos/clear-completed`);
      fetchTodos(filter);
    } catch (error) {
      console.error("清除已完成失败:", error);
    }
  };

  // 清除全部
  const clearAll = async () => {
    try {
      await axios.delete(`${API_BASE_URL}/todos/clear-all`);
      fetchTodos(filter);
    } catch (error) {
      console.error("清除全部失败:", error);
    }
  };

  // 处理回车添加
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      addTodo();
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-title">📝 待办事项</h1>

      {/* 添加表单 */}
      <div className="add-form">
        <input
          type="text"
          placeholder="输入新的待办事项..."
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          onKeyPress={handleKeyPress}
          className="todo-input"
          disabled={loading}
        />
        <button
          className="add-btn"
          onClick={addTodo}
          disabled={loading || !newTodo.trim()}
        >
          添加
        </button>
      </div>

      {/* 筛选按钮 */}
      <div className="filter-buttons">
        <button
          className={`filter-btn ${filter === "all" ? "active" : ""}`}
          onClick={() => setFilter("all")}
        >
          全部 ({todos.length})
        </button>
        <button
          className={`filter-btn ${filter === "pending" ? "active" : ""}`}
          onClick={() => setFilter("pending")}
        >
          未完成 ({todos.filter((t) => !t.completed).length})
        </button>
        <button
          className={`filter-btn ${filter === "completed" ? "active" : ""}`}
          onClick={() => setFilter("completed")}
        >
          已完成 ({todos.filter((t) => t.completed).length})
        </button>
      </div>

      {/* 待办事项列表 */}
      <ul className="todo-list">
        {todos.length === 0 ? (
          <li className="empty-state">暂无待办事项，添加一个吧！</li>
        ) : (
          todos.map((todo) => (
            <li
              key={todo.id}
              className={`todo-item ${todo.completed ? "completed" : ""}`}
            >
              <span className="todo-title">{todo.title}</span>
              <div className="todo-actions">
                <button
                  className="complete-btn"
                  onClick={() => toggleComplete(todo)}
                >
                  {todo.completed ? "撤销" : "完成"}
                </button>
                <button
                  className="delete-btn"
                  onClick={() => deleteTodo(todo.id)}
                >
                  删除
                </button>
              </div>
            </li>
          ))
        )}
      </ul>

      {/* 底部操作按钮 */}
      <div className="bottom-actions">
        <button className="clear-btn" onClick={clearCompleted}>
          清除已完成
        </button>
        <button className="clear-btn clear-all-btn" onClick={clearAll}>
          清除全部
        </button>
      </div>
    </div>
  );
}

export default App;
