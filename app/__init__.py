# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
admin = Admin(app)


from .admin import admin_blueprint
from .auth import auth_blueprint
from .api import api_blueprint
from .dashboard import dashboard_blueprint


app.register_blueprint(admin_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(dashboard_blueprint)


from app import models
