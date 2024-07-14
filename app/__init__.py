import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from app.db_connection import mongo
from app.routes.teams import teams
from app.routes.index import index
from app.routes.astra import astra
from app.routes.users import users

# TODO create custom logger

def create_app():
    # Loading env vars
    print(f'Loading environment variables...')
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", "config", 'dev.env') # TODO dev.env shouldnt be hardcoded
    load_dotenv(dotenv_path)


    # Creating flask app and loading env vars
    print('Creating app...')
    app = Flask(__name__)   
    load_env_vars_onto_app(app, dotenv_path)
    CORS(app, support_credentials=True)
  
    # Setup db connection
    print('Setting up db connection...')
    print(os.getenv('MONGO_URI'))
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    mongo.init_app(app) 

    # Register blueprints
    app.register_blueprint(teams, url_prefix='/teams')
    app.register_blueprint(index, url_prefix='/')
    app.register_blueprint(astra, url_prefix='/astra')
    app.register_blueprint(users, url_prefix='/users')

    return app

def load_env_vars_onto_app(app, dotenv_path):
    env_vars = dotenv_to_dict(dotenv_path)
    for key, value in env_vars.items():
        app.config[key] = value

def dotenv_to_dict(dotenv_path):
    env_vars = {}
    with open(dotenv_path) as f:
        for line in f:
            key, value = line.split("=")
            env_vars[key] = value
    return env_vars
