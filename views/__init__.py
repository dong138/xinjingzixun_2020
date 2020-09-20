from flask import Blueprint

index_blu = Blueprint("index_blu", __name__)

from . import index
