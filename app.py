from flask import Flask
from flask_cors import CORS
from config.db import db as conf_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = conf_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, resources={r"/*": {"origins": "*", "expose_headers": "*"}})
