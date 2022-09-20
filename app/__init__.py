from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)


# Base = declarative_base()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///..\\database\\property.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)





