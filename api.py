from flask_potion import ModelResource, fields
from flask_potion import Api
from models import *
from app import app


class UserResource(ModelResource):
    class Meta:
        model = User
        natural_key = 'username'


class HostResource(ModelResource):
    class Meta:
        model = Host
        natural_key = 'hostname'


class SessionResource(ModelResource):
    class Meta:
        model = Session

    class Schema:
        user = fields.Inline('user')
        host = fields.Inline('host')
        uuid = fields.UUID()
        start = fields.DateTimeString()
        end = fields.DateTimeString()
        duration = fields.Custom('{"type": "number"}', io="r", formatter=lambda x: x.total_seconds())


class CommandResource(ModelResource):
    class Meta:
        model = Command
        natural_key = 'cmd'

    class Schema:
        timing = fields.DateTimeString()
        session = fields.ToOne('session')


api = Api(app)
api.add_resource(UserResource)
api.add_resource(HostResource)
api.add_resource(SessionResource)
api.add_resource(CommandResource)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
