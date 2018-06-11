from flask_potion import ModelResource, fields, Api
from flask_potion.routes import Relation, Route
from models import *
from app import app
from config import path
import base64

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
        postgres_text_search_fields = ('uuid')

    class Schema:
        uuid = fields.UUID()
        user = fields.Inline('user')
        host = fields.Inline('host')
        start = fields.DateTimeString()
        end = fields.DateTimeString()
        duration = fields.Custom('{"type": "integer"}', io="r", formatter=lambda x: x.total_seconds())

    @Route.GET('/by_command')
    def session_by_command(self, cmd: fields.String(), **kwargs) -> fields.List(fields.Inline('self')):
        return Session.query.join(Command).filter(Command.cmd.like('%{0}%'.format(cmd)))

    @Route.GET('/log')
    def session_log(self, session_uuid: fields.UUID()) -> fields.String():
        session = Session.query.filter(Session.uuid == session_uuid).first()
        session_log_path = path.session_logs + session.start.date().isoformat().replace('-', '') + '/' + \
            session.user.username + '_' + session.host.hostname + '_' + \
            session.start.time().isoformat().split('.')[0].replace(':', '') + '_' + \
            session_uuid + '.log'
        with open(session_log_path, 'rb') as session_log:
            return base64.b64encode(session_log.read()).decode('utf-8', 'strict')

    @Route.GET('/timed_log')
    def session_timed_log(self, session_uuid: fields.UUID()) -> fields.List(fields.String()):
        session = Session.query.filter(Session.uuid == session_uuid).first()
        session_base_path = path.session_logs + session.start.date().isoformat().replace('-', '') + '/' + \
            session.user.username + '_' + session.host.hostname + '_' + \
            session.start.time().isoformat().split('.')[0].replace(':', '') + '_' + \
            session_uuid
        session_log_path = session_base_path + '.log'
        session_timer_path = session_base_path + '.timer'
        results = []
        session_time = 0.
        session_seek = 0
        with open(session_log_path, 'rb') as session_log:
            with open(session_timer_path, 'r') as session_timer:
                session_data = session_log.read()
                # todo improve this (use csv reader?)
                lines = session_timer.readlines()
                for l in lines:
                    rel_time, rel_seek = l.split(' ')
                    rel_time = float(rel_time)
                    rel_seek = int(rel_seek)
                    session_time += rel_time
                    current_seek = session_seek
                    session_seek += rel_seek
                    results.append({
                        'session_time': session_time,
                        'session_seek': session_seek,
                        'session_size': len(session_data),
                        'data_size': rel_seek,
                        'data': base64.b64encode(session_data[current_seek:session_seek]).decode('utf-8', 'strict')
                    })
        return results


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
