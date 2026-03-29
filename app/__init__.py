from flask import Flask
from .config import Config
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from .models import db


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

from app import views