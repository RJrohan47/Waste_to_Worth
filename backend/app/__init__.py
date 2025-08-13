from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv() # load environment variable from .env
 
# creating db and jwt instances 
db = SQLAlchemy()
jwt=JWTManager()

def create_app():
    app = Flask(__name__)
    # database congfig
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #Security keys
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')
    app.config['JWT_SECRET_KEY']= os.environ.get('JWT_SECRET_KEY','super-secret-jwt-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES']=3600 # Token expires in 1 hour 
    # enable CORS
    CORS(app)
    

    # Init extensions
    db.init_app(app)

    jwt.init_app(app)

    # Register models
    from . import models # importing whole models package 


    # Registered blueprints
    from .routes.auth_routes import auth_bp # import the auth_routes module inside routes package 
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app

__all__ = ['db','jwt','create_app']
