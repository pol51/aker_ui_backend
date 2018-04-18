#!/usr/bin/env python

from models import *
from utils import DB
from datetime import datetime

def import_session_from_file(filename):
    db = DB()
    def get_datetime(cmd, value):
        return datetime.strptime(cmd[value], '%Y/%m/%d %H:%M:%S')

    with open(filename, 'r') as file:
        # load json objects (commands)
        import json
        commands = [json.loads(l) for l in file.readlines()]
        if len(commands) < 1:
            raise Exception('no command in {}'.format(filename))

        last_cmd = commands[-1]

        # load or create user
        username = last_cmd['user']
        user = db.connetion.query(User).filter(User.username == username).first()
        if user is None:
            user = User(username)
            db.connetion.add(user)
            db.connetion.commit()

        # load or create host
        hostname = last_cmd['host']
        host = db.connetion.query(Host).filter(Host.hostname == hostname).first()
        if host is None:
            host = Host(hostname)
            db.connetion.add(host)
            db.connetion.commit()

        # check session already exists
        session_uuid = last_cmd['session']
        session = db.connetion.query(Session).filter(Session.uuid == session_uuid).first()
        if session:
            raise Exception('session already loaded ({})'.format(filename))

        # create session
        start = get_datetime(last_cmd, 'sessionstart')
        end = get_datetime(last_cmd, 'sessionend')
        session = Session(session_uuid, user, host, start, end)
        db.connetion.add(session)

        # create commands
        for command in commands[:-1]:
            cmd = Command(session, command['cmd'], get_datetime(command, 'timing'))
            db.connetion.add(cmd)

        db.connetion.commit()
    pass


if __name__ == '__main__':
    from sys import argv
    import_session_from_file(argv[1])
