# graphql/resolvers.py
from models import ToDoModel

def resolve_todos(self, info):
    return ToDoModel.query.all()

def mutate_create_todo(self, info, title, description, time):
    todo = ToDoModel(title=title, description=description, time=time)
    db.session.add(todo)
    db.session.commit()
    return CreateToDo(todo=todo)

def mutate_delete_todo(self, info, id):
    todo = ToDoModel.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return DeleteToDo(success=True)
    else:
        return DeleteToDo(success=False)

def mutate_edit_todo(self, info, id, title=None, description=None, time=None):
    todo = ToDoModel.query.get(id)
    if todo:
        if title:
            todo.title = title
        if description:
            todo.description = description
        if time:
            todo.time = time
        db.session.commit()
        return EditToDo(todo=todo)
    else:
        return EditToDo(todo=None)
