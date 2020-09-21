from flask import render_template

from models import db
from models.index import News

from . import index_blu


# 用app.route添加路由
@index_blu.route("/")
def index():
    # return "我是第一个网页...new"
    news = db.session.query(News).first()
    print("--------->", news)
    return render_template("index.html")
