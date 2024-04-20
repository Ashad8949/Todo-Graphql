# graphql/schema.py
import graphene


class ToDo(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    time = graphene.String()
    image = graphene.String()


class Query(graphene.ObjectType):
    todos = graphene.List(ToDo)

    def resolve_todos(self, info):
        # Implement logic to fetch all To-Do items from database
        pass


class CreateToDo(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        time = graphene.String()

    todo = graphene.Field(ToDo)

    def mutate(self, info, title, description, time):
        # Implement logic to create a new To-Do item
        pass


class DeleteToDo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()

    def mutate(self, info, id):
        # Implement logic to delete a To-Do item
        pass


class EditToDo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        description = graphene.String()
        time = graphene.String()

    todo = graphene.Field(ToDo)

    def mutate(self, info, id, title=None, description=None, time=None):
        # Implement logic to edit a To-Do item
        pass


class Mutation(graphene.ObjectType):
    create_todo = CreateToDo.Field()
    delete_todo = DeleteToDo.Field()
    edit_todo = EditToDo.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
