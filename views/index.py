from flask import render_template, jsonify, request, session

from models import db
from models.index import News

from . import index_blu


# 用app.route添加路由
@index_blu.route("/")
def index():
    # return "我是第一个网页...new"
    clicks_top_6_news = db.session.query(News).order_by(-News.clicks).limit(6)
    # 提取session，以验证用户是否登录成
    user_id = session.get("user_id")
    nick_name = session.get("nick_name")

    return render_template("index.html", clicks_top_6_news=clicks_top_6_news, nick_name=nick_name)


@index_blu.route("/newslist")
def news_list():
    # 1. 提取数据
    page = int(request.args.get("page"))
    cid = int(request.args.get("cid")) + 1
    per_page = int(request.args.get("per_page"))

    # 2. 根据前端传递过来的参数，查询数据库
    # 且 创建了paginate对象，这个对象中有分页需要的所有信息
    # 如果是要查询最新的信息，那么按照新闻的update_time进行倒叙排序，而不是找这个分类
    if cid == 1:
        paginate = db.session.query(News).order_by(-News.update_time).paginate(page, per_page, False)
    else:
        paginate = db.session.query(News).filter(News.category_id == cid).paginate(page, per_page, False)

    ret = {
        "totalPage": paginate.pages,  # 总页数
        "newsList": [news.to_dict() for news in paginate.items]
    }

    return jsonify(ret)  # 将python中的字典 转换为字符串，且这个字符串的格式是很类似字典的，这种格式叫做json


@index_blu.route("/detail/<int:news_id>")
def detail(news_id):
    # 根据id找到这篇新闻
    news = db.session.query(News).filter(News.id == news_id).first()

    # 提取session，以验证用户是否登录成
    user_id = session.get("user_id")
    nick_name = session.get("nick_name")

    # 既然News模型类中已经添加了与User模型类关联的代码，即relationship那句话，此时就意味着可以通过News对象找到对应User对象
    # 根据news对象，找作者
    # print(news.user.nick_name)
    news_author = news.user
    news_author.news_num = news_author.news.count()
    news_author.followers_num = news_author.followers.count()
    news_author.can_follow = user_id not in [x.id for x in news_author.followers]

    return render_template("detail.html", news=news, nick_name=nick_name, news_author=news_author)
