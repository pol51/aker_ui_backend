from flask_potion import ModelResource, fields, Api
from flask_potion.routes import Relation
from models import *
from app import app


class UserResource(ModelResource):
    sessions = Relation('session')

    class Meta:
        model = User
        natural_key = 'username'


class HostResource(ModelResource):
    sessions = Relation('session')

    class Meta:
        model = Host
        natural_key = 'hostname'


class SessionResource(ModelResource):
    commands = Relation('command')

    class Meta:
        model = Session

    class Schema:
        uuid = fields.UUID()
        user = fields.Inline('user')
        host = fields.Inline('host')
        start = fields.DateTimeString()
        end = fields.DateTimeString()
        duration = fields.Custom('{"type": "integer"}', io="r", formatter=lambda x: x.total_seconds())


class CommandResource(ModelResource):
    class Meta:
        model = Command
        natural_key = 'cmd'

    class Schema:
        timing = fields.DateTimeString()
        session = fields.ToOne('session')


api = Api(app)
api.add_resource(CommandResource)
api.add_resource(SessionResource)
api.add_resource(UserResource)
api.add_resource(HostResource)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
