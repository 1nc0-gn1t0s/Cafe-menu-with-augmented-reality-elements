from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.secret_key = 'there will be something here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafeAR.db'
db = SQLAlchemy(app)
