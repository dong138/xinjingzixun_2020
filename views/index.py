from flask import render_template,jsonify

from models import db
from models.index import News

from . import index_blu


@index_blu.route("/")
def index():
    # 查询点击量最多的前6个新闻信息
    clicks_top_6_news = db.session.query(News).order_by(-News.clicks).limit(6)
    return render_template("index.html", clicks_top_6_news=clicks_top_6_news)


@index_blu.route("/newslist")
def category_news():
    ret = {
        "totalPage": 2,
        "newsList": [
            {
                "id": 1,
                "title": "我是测试新闻1",
                "index_image_url": "",
                "digest": "这个新闻很棒.......",
                "create_time": "2020年09月21日",
                "source": "王老师日报"
            },
            {
                "id": 2,
                "title": "我是测试新闻2",
                "index_image_url": "",
                "digest": "这个新闻很棒2.......",
                "create_time": "2020年09月22日",
                "source": "王老师日报2"
            }
        ]
    }
    return jsonify(ret)
