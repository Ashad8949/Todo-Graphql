from models import ToDoModel
from database import db

def list_todos(self, info):
    return ToDoModel.query.all()


def create_todo(info, title, description, time):
    new_todo = ToDoModel(title=title, description=description, time=time)
    db.session.add(new_todo)
    db.session.commit()
    return {'todo': new_todo}


def delete_todo(info, id):
    todo = ToDoModel.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return {'success': True}
    return {'success': False}


def edit_todo(info, id, title=None, description=None, time=None):
    todo = ToDoModel.query.get(id)
    if todo:
        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if time is not None:
            todo.time = time
        db.session.commit()
        return {'todo': todo}
    return {'todo': None}
