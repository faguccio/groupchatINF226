import flask 
import apsw
from apsw import Error
from threading import local
from pygments.formatters import HtmlFormatter
import os
import logging
import time


logging.basicConfig(filename='mordor.log', encoding='utf-8', level=logging.INFO)
logging.info(f"Server started at {time.time()}") 
DATABASE_path = "./tiny.db"


tls = local()
cssData = HtmlFormatter(nowrap=True).get_style_defs('.highlight')
conn = None


app = flask.Flask(__name__)
app.secret_key = os.urandom(24)


import flask_login

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from flask_login import login_required, login_user, logout_user
from login_form import LoginForm


ALL_address = "#all"