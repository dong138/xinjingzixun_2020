from flask import render_template

from . import index_blu


# 用app.route添加路由
@index_blu.route("/")
def index():
    # return "我是第一个网页...new"
    return render_template("index.html")
