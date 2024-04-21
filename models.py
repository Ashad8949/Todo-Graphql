# models.py
from graphql_api import db  # Import db from your Flask app


class ToDoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255))

    def __repr__(self):
        return f'<ToDo {self.id}>'
