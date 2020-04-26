from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__, static_folder='assets')
app.config.from_object(Config)

from app import pages

bootstrap = Bootstrap(app)
