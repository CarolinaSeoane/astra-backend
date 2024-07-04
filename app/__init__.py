import os
from dotenv import load_dotenv
from flask import Flask, Blueprint
from flask_pymongo import PyMongo

from app.routes.teams import teams
from app.routes.index import index
# TODO create custom logger

def create_app():
    # Loading env vars
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", "config", 'dev.env') # TODO dev.env shouldnt be hardcoded
    load_dotenv(dotenv_path)
    print(f"the dotenv path: {dotenv_path}")
    
    print("creating app")
    app = Flask(__name__)
    load_env_vars_onto_app(app, dotenv_path)

    # Setup db connection

    # Register blueprints
    app.register_blueprint(teams, url_prefix='/teams')
    app.register_blueprint(index, url_prefix='/')

    return app

def load_env_vars_onto_app(app, dotenv_path):
    env_vars = dotenv_to_dict(dotenv_path)
    for key, value in env_vars.items():
        print(f"found key {key} with value {value}")
        app.config[key] = value

def dotenv_to_dict(dotenv_path):
    env_vars = {}
    with open(dotenv_path) as f:
        for line in f:
            key, value = line.split("=")
            env_vars[key] = value
    return env_vars
