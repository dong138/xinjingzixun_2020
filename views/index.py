from flask import render_template, jsonify, request

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
    # 1. 获取前端传递过来的数据，就是提取 URL中的数据
    # http://127.0.0.1:8899/newslist?page=1&cid=1&per_page=10
    # 要从上述URL中提取page、cid、per_page的值
    page = request.args.get('page', 1)  # 前端要的是哪一页的数据
    cid = request.args.get('cid', 0)  # 前端要的是哪个分类的数据，是股市、债市还是商品、外汇、公司
    per_page = request.args.get('per_page', 1)  # 前端要的是每一页中的新闻个数

    # 2. 到数据库中查询数据
    paginate = db.session.query(News).paginate(page=int(page), per_page=int(per_page), error_out=False)

    # 3. 准备好要返回给浏览器的数据
    ret = {
        "totalPage": paginate.pages,  # 总页数
        "newsList": []
    }

    # 4. 遍历当前页中新闻信息,最终的目的取新闻对象中的属性，将其封装到字典中
    for news in paginate.items:
        temp_dit = dict()
        temp_dit["id"] = news.id
        temp_dit["digest"] = news.digest
        temp_dit["create_time"] = news.create_time
        temp_dit["index_image_url"] = news.index_image_url
        temp_dit["source"] = news.source
        temp_dit["title"] = news.title

        # 将得到的字典，添加到ret中newsList对应的列表中
        ret['newsList'].append(temp_dit)

    # 5. 将ret字典转换为json样子的字符串，返回
    return jsonify(ret)
