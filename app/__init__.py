import os, logging, sys

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'bti.sqlite'),
    )

    if test_config is None: # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else: # load the test config if passed in
        app.config.from_mapping(test_config)

    try: # ensure the instance folder exists
        datasets = os.path.join(app.instance_path, 'datasets')
        os.makedirs(datasets, exist_ok=True)
        os.makedirs(os.path.join(datasets, 'zips'), exist_ok=True)
        os.makedirs(os.path.join(datasets, 'raw'), exist_ok=True)
        os.makedirs(os.path.join(datasets, 'wrangled'), exist_ok=True)
    except OSError as e:
        print(e)
        pass

    bootstrap = Bootstrap(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app