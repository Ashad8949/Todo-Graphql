from flask import Flask, render_template
from database import db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,  template_folder='../template', static_folder='../static')
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ztuxaxua:W8_bCQdESb23wUnajthCxa8NE9dPbzke@snuffleupagus.db.elephantsql.com/ztuxaxua"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)




