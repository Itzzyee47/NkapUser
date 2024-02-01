from flask import Flask
from firebase_admin import credentials,initialize_app, firestore, storage

cred = credentials.Certificate("api/key1.json")

default_app = initialize_app(cred, {'storageBucket': 'gs://nkap-4181f.appspot.com'})

def create_app():
    app = Flask(__name__) 
    app.config['SECRET_KEY'] = '123qwert'
    
    from .userApi import userAPI
    
    app.register_blueprint(userAPI, url_prefix='/')
    
    return app
