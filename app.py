from flask_graphql import GraphQLView

from graphql_api import app, db
from graphql_api.schema import schema

# Create an application context
with app.app_context():
    # Create all database tables
    db.create_all()
@app.route('/graphql', methods=['GET', 'POST'])
def graphql_view():
    return GraphQLView.as_view('graphql', schema=schema, graphiql=True)()

if __name__ == '__main__':
    app.run(debug=True)
