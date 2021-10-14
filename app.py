from flask import Flask
from os import getenv
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

csrf = CSRFProtect()
csrf.init_app(app)

import routes