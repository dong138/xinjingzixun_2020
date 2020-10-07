from flask import jsonify, request, session

from models import db
from models.index import Collection
from . import news_blu


@news_blu.route("/news/collect", methods=["POST"])
def news_collect():
    # 1. 提取数据（action、news_id、user_id）
    action = request.json.get("action")
    news_id = request.json.get("news_id")
    user_id = session.get("user_id")

    # 2. 根据操作时收藏、取消收藏 进行不同的操作
    if action == "do":
        collection = Collection()
        collection.user_id = user_id
        collection.news_id = news_id
        db.session.add(collection)
        db.session.commit()

        # 3. 返回对应的信息
        ret = {
            "errno": 0,
            "errmsg": "成功"
        }
    elif action == "undo":
        collection = db.session.query(Collection).filter(Collection.news_id == news_id, Collection.user_id == user_id).first()
        db.session.delete(collection)
        db.session.commit()
        # 3. 返回对应的信息
        ret = {
            "errno": 0,
            "errmsg": "成功"
        }

    return jsonify(ret)
