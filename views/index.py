from flask import render_template

from models import db
from models.index import News

from . import index_blu


# 用app.route添加路由
@index_blu.route("/")
def index():
    # return "我是第一个网页...new"
    clicks_top_6_news = db.session.query(News).order_by(-News.clicks).limit(6)
    # print("--------->", news)
    return render_template("index.html", clicks_top_6_news=clicks_top_6_news)
