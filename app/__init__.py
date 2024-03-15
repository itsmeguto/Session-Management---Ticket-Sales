# app/__init__.py
from flask import Flask
import redis
import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(app):
    # Create logs directory if it does not exist
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Set up log file handler
    file_handler = RotatingFileHandler('logs/ticket_app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

    # Set the logging level and add the file handler to app logger
    file_handler.setLevel(logging.INFO)  # Change to DEBUG for more detailed logs
    app.logger.addHandler(file_handler)

    # Log that logging is set up
    app.logger.info('Ticket app logging is set up')

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    
    if config_filename:
        app.config.from_pyfile(config_filename, silent=True)
    
    app.config.setdefault('REDIS_HOST', 'localhost')
    app.config.setdefault('REDIS_PORT', 6379)
    app.config.setdefault('REDIS_DB', 0)

    app.redis = redis.Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB']
    )

    # Import routes after the app has been initialized
    from .routes import bp
    app.register_blueprint(bp)

    configure_logging(app)

    return app
