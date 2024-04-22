import json
from flask import redirect, url_for, session, render_template,abort
from flask_graphql import GraphQLView
from graphql_api import app, db
from graphql_api.schema import schema
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode

app.secret_key = 'your_secret_key'
appConf = {
    "OAUTH2_CLIENT_ID": "todo",
    "OAUTH2_CLIENT_SECRET": "KNHy9PFd2peoIAs94mMwL8Erp7nBDBcO",
    "OAUTH2_ISSUER": "http://localhost:8080/realms/myrelm",
    "FLASK_SECRET": "ALongRandomlyGeneratedString",
    "FLASK_PORT": 5000
}

app.secret_key = appConf.get("FLASK_SECRET")

oauth = OAuth(app)
oauth.register(
    "myApp",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
        # 'code_challenge_method': 'S256'  # enable PKCE
    },
    server_metadata_url=f'{appConf.get("OAUTH2_ISSUER")}/.well-known/openid-configuration',
)


@app.route("/")
def home():
    return render_template(
        "index.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )



# Initialize Flask-GraphQL
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

@app.route("/callback")
def callback():
    token = oauth.myApp.authorize_access_token()
    session["user"] = token
    return redirect(url_for("home"))

@app.route("/login")
def login():
    # check if session already present
    if "user" in session:
        abort(404)
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("callback", _external=True))


@app.route("/loggedout")
def loggedOut():
    # check if session already present
    if "user" in session:
        abort(404)
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    id_token = session["user"]["id_token"]
    session.clear()
    return redirect(
        appConf.get("OAUTH2_ISSUER")
        + "/protocol/openid-connect/logout?"
        + urlencode(
            {
                "post_logout_redirect_uri": url_for("loggedOut", _external=True),
                "id_token_hint": id_token
            },
            quote_via=quote_plus,
        )
    )


if __name__ == '__main__':
    app.run(debug=True)
