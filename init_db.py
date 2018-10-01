#!/usr/bin/env python

from models import *
from utils import DB
from db import db as model_db

if __name__ == '__main__':
    db_con = DB()
    model_db.Model.metadata.create_all(db_con.engine)
