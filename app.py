import json
import stripe
from flask import redirect, url_for, session, render_template, abort, jsonify
from flask_graphql import GraphQLView
from graphql_api import app
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

stripe_keys = {
    "publishable_key": "pk_test_51P8QFkSAQxKJZ34tJiOcX9ZulhAAbcYsBo2SM9UI3zgpXHW3NNKEJ9CgdMHxT9tvdB3EhgHrRZQ6lQtxemoOLmze00L6kHK6rP",
    "secret_key": "sk_test_51P8QFkSAQxKJZ34tp7EcgEauz3LgqsC3T0achtgzQmbsJFzZ8WSoGeyNW92LzYW6x1O0P7GYQydpHEgnBO1Ugnq400g5lnJVdP",
}

stripe.api_key = stripe_keys["secret_key"]

oauth = OAuth(app)
oauth.register(
    "myApp",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
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


@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    domain_url = "http://127.0.0.1:5000/"
    try:
        # Create new Checkout Session for the order
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": "price_1P8QR2SAQxKJZ34tzJu8Ztj2",
                    "quantity": 1,
                }
            ]
        )
    except Exception as e:
        return jsonify(error=str(e)), 500
    return redirect(checkout_session.url, code=303)


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/cancelled")
def cancelled():
    return render_template("cancelled.html")


if __name__ == '__main__':
    app.run(debug=True)
