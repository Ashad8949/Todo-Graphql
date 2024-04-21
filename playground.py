# app.py
from flask import Flask
from flask_graphql import GraphQLView
import graphene


# Define your GraphQL schema using Graphene
class Query(graphene.ObjectType):
    hello = graphene.String(description='a typical hello world')

    def resolve_hello(self, info):
        return f"Hello ashad"


# schema = graphene.Schema(query=Query)

app = Flask(__name__)
# app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == "__main__":
    app.run(debug=True)
