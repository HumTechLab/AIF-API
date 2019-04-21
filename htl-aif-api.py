#!/usr/bin/env python3
# Built on work by https://github.com/thomaxxl
# Adapted by HTL @ TU Delft
#
import sys, logging, inspect, builtins
from sqlalchemy import INTEGER, CHAR, Column, DateTime, Float, ForeignKey, Index, Integer, String, TIMESTAMP, Table, Text, UniqueConstraint, text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect
from flask_swagger_ui import get_swaggerui_blueprint
from safrs import SAFRSBase, jsonapi_rpc, SAFRSJSONEncoder, Api, SAFRSAPI
from safrs import search, startswith

db = SQLAlchemy()
app = Flask('HumTechLab AIF API')
app.config.update( SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test1:test1-@localhost/test1', DEBUG = True)
app.url_map.strict_slashes = False
SAFRSBase.db_commit = False
builtins.db  = SQLAlchemy(app)

class Hazard(SAFRSBase, db.Model):
    '''
        description: Dummy description
    '''
    __tablename__ = 'hazards'

    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    polygon_coordinates = Column(String(255), nullable=False)
    severity = Column(String(255), nullable=False)

class UshahidiReport(SAFRSBase, db.Model):
    '''
        description: Dummy description
    '''
    __tablename__ = 'ushahidi_reports'

    id = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False)
    submitted_by = Column(String(255), nullable=False)
    submitted_on = Column(String(255), nullable=False)

if __name__ == '__main__':
    HOST = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
    PORT = 5000
    db.init_app(app)
    db.app = app
    # Create the database
    db.create_all()
    API_PREFIX = ''

    with app.app_context():
        api = SAFRSAPI(app, host='{}:{}'.format(HOST,PORT), port=PORT, prefix=API_PREFIX)
        # Expose the database objects as REST API endpoints
        api.expose_object(UshahidiReport)
        api.expose_object(Hazard)
        # Register the API at /api/docs
        print('Starting API: http://{}:{}{}'.format(HOST, PORT, API_PREFIX))
        app.run(host=HOST, port=PORT)
