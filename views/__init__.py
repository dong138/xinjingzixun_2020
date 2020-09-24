from flask import Blueprint

index_blu = Blueprint("index_blu", __name__)
passport_blu = Blueprint("passport_blu", __name__)
user_blu = Blueprint("user_blu", __name__)

from . import index
from . import passport
from . import user
