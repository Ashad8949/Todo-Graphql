import graphene
from models import ToDoModel  # Import ToDoModel from models.py
from graphql_api import resolvers


class ToDo(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    time = graphene.String()
    image = graphene.String()


class Query(graphene.ObjectType):
    todos = graphene.List(ToDo, resolver=resolvers.list_todos)


class CreateToDo(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        time = graphene.String()

    todo = graphene.Field(ToDo)

    def mutate(self, info, title, description, time):
        return resolvers.create_todo(info, title, description, time)


class DeleteToDo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()

    def mutate(self, info, id):
        return resolvers.delete_todo(info, id)


class EditToDo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        description = graphene.String()
        time = graphene.String()

    todo = graphene.Field(ToDo)

    def mutate(self, info, id, title=None, description=None, time=None):
        return resolvers.edit_todo(info, id, title, description, time)


class Mutation(graphene.ObjectType):
    create_todo = CreateToDo.Field()
    delete_todo = DeleteToDo.Field()
    edit_todo = EditToDo.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
