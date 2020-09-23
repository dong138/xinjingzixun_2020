from flask import render_template, jsonify, request, session

from models import db
from models.index import News

from . import index_blu


@index_blu.route("/")
def index():
    # 查询点击量最多的前6个新闻信息
    clicks_top_6_news = db.session.query(News).order_by(-News.clicks).limit(6)

    # 查询用户是否已经登录
    user_id = session.get("user_id", 0)
    nick_name = session.get("nick_name", "")

    return render_template("index.html", clicks_top_6_news=clicks_top_6_news, nick_name=nick_name)


@index_blu.route("/newslist")
def category_news():
    # 1. 获取前端传递过来的数据，就是提取 URL中的数据
    # http://127.0.0.1:8899/newslist?page=1&cid=1&per_page=10
    # 要从上述URL中提取page、cid、per_page的值
    page = request.args.get('page', 1)  # 前端要的是哪一页的数据
    cid = int(request.args.get('cid', 0))  # 前端要的是哪个分类的数据，是股市、债市还是商品、外汇、公司
    per_page = request.args.get('per_page', 1)  # 前端要的是每一页中的新闻个数

    # 2. 到数据库中查询数据
    # 如果cid是0，表示要看最新的，如果不是0则按照原来规则查询
    if cid == 0:
        paginate = db.session.query(News).order_by(-News.clicks).paginate(page=int(page), per_page=int(per_page), error_out=False)
    else:
        cid += 1  # 由于测试数据分类中从0开始，而数据库中是从1开始的，所以用户点击的1实际上是2
        paginate = db.session.query(News).filter(News.category_id == cid).paginate(page=int(page), per_page=int(per_page), error_out=False)

    # 3. 准备好要返回给浏览器的数据
    ret = {
        "totalPage": paginate.pages,  # 总页数
        "newsList": [news.to_dict() for news in paginate.items]
    }

    # 4. 将ret字典转换为json样子的字符串，返回
    return jsonify(ret)


@index_blu.route("/detail/<int:news_id>")
def detail(news_id):
    # 根据news_id查询这个新闻的详情
    news = db.session.query(News).filter(News.id == news_id).first()

    # 查询这个新闻的作者
    news_author = news.user
    news_author.news_num = news_author.news.count()
    news_author.follwer_num = news_author.followers.count()

    # 查询用户是否已经登录
    user_id = session.get("user_id", 0)
    nick_name = session.get("nick_name", "")

    # 计算当前登录用户是否已经关注了这个新闻的作者
    news_author_followers_id = [x.id for x in news_author.followers]
    if user_id in news_author_followers_id:
        news_author.can_follow = False  # 已经关注了作者，就不能在关注了
    else:
        news_author.can_follow = True  # 可以关注

    return render_template("detail.html", news=news, nick_name=nick_name, news_author=news_author)
