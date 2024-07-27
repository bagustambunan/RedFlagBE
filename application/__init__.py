from flask import Flask

app = Flask("application")

from application.controllers import *
from application.models import *