
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

admin = Admin(app)


from app import views
from app import models