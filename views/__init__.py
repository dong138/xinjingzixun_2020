from flask import Blueprint

index_blu = Blueprint("index", __name__)
passport_blu = Blueprint("passport", __name__)

from . import index
from . import passport
