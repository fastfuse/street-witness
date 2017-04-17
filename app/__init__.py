
import os
import pymongo
from flask import Flask
from flask_admin import Admin


app = Flask(__name__)

admin = Admin(app)

app.config.from_object('config.DevelopmentConfig')

# pymongo db instance
client = pymongo.MongoClient()
db = client['street-witness']



from app import views
