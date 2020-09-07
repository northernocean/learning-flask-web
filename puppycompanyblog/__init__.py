from flask import Flask
from puppycompanyblog.core.views import core
from puppycompanyblog.error_pages.handlers import error_pages

app = Flask(__name__)

app.register_blueprint(core)
app.register_blueprint(error_pages)
