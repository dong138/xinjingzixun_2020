from . import index_blu


@index_blu.route("/")
def index():
    return "我是主页...new"
