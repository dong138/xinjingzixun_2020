from flask import render_template

from models import db
from models.index import News

from . import index_blu


@index_blu.route("/")
def index():
    # 查询点击量最多的前6个新闻信息
    clicks_top_6_news = db.session.query(News).order_by(-News.clicks).limit(6)
    return render_template("index.html", clicks_top_6_news=clicks_top_6_news)
