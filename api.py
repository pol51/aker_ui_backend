from flask import Flask
from flask_restless import APIManager
from utils import DB
from models import *

db = DB()
Base.metadata.bind = db.engine


def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Access-Control-Allow-Origin, Content-Type, Accept'
    return response


app = Flask(__name__)
app.after_request(add_cors_header)
apimanager = APIManager(app, session=db.connetion)
user_api_blueprint = apimanager.create_api_blueprint(User, methods=['GET'])
host_api_blueprint = apimanager.create_api_blueprint(Host, methods=['GET'])
session_api_blueprint = apimanager.create_api_blueprint(Session, methods=['GET'])
command_api_blueprint = apimanager.create_api_blueprint(Command, methods=['GET'])

if __name__ == '__main__':
    app.register_blueprint(user_api_blueprint)
    app.register_blueprint(host_api_blueprint)
    app.register_blueprint(session_api_blueprint)
    app.register_blueprint(command_api_blueprint)

    app.run(host='0.0.0.0', port=8888, debug=True)
