from crud import get_todos, create_todo, update_todo, delete_todo, clear_completed_todos, clear_all_todos
from schemas import TodoCreate, TodoUpdate


def test_create_todo(db):
    todo_create = TodoCreate(title="Test item")
    todo = create_todo(db, todo_create)

    assert todo.id is not None
    assert todo.title == "Test item"
    assert todo.completed is False


def test_get_todos_filters(db):
    clear_all_todos(db)

    create_todo(db, TodoCreate(title="Pending 1", completed=False))
    create_todo(db, TodoCreate(title="Completed 1", completed=True))
    create_todo(db, TodoCreate(title="Pending 2", completed=False))

    all_todos = get_todos(db, status="all")
    pending_todos = get_todos(db, status="pending")
    completed_todos = get_todos(db, status="completed")

    assert len(all_todos) == 3
    assert len(pending_todos) == 2
    assert len(completed_todos) == 1


def test_update_todo_and_missing(db):
    clear_all_todos(db)

    todo = create_todo(db, TodoCreate(title="Original"))
    todo_update = TodoUpdate(title="Updated", completed=True)
    updated = update_todo(db, todo.id, todo_update)

    assert updated is not None
    assert updated.title == "Updated"
    assert updated.completed is True

    assert update_todo(db, 9999, TodoUpdate(completed=True)) is None


def test_delete_todo(db):
    clear_all_todos(db)

    todo = create_todo(db, TodoCreate(title="To delete"))
    assert delete_todo(db, todo.id) is True
    assert delete_todo(db, todo.id) is False


def test_clear_completed_and_all(db):
    clear_all_todos(db)

    create_todo(db, TodoCreate(title="Complete me", completed=True))
    create_todo(db, TodoCreate(title="Keep me", completed=False))

    deleted_completed = clear_completed_todos(db)
    assert deleted_completed == 1
    assert len(get_todos(db)) == 1

    deleted_all = clear_all_todos(db)
    assert deleted_all == 1
    assert len(get_todos(db)) == 0
