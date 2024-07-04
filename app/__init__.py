from flask import Flask, Blueprint
from flask_pymongo import PyMongo

from app.routes.teams import teams
from app.routes.index import index

def create_app():
    app = Flask(__name__)

    # Load configuration

    # Setup db connection

    # Register blueprints
    app.register_blueprint(teams, url_prefix='/teams')
    app.register_blueprint(index, url_prefix='/')

    return app
