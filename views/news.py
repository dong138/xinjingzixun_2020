from flask import jsonify, request, session

from models import db
from models.index import Collection, Comment
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


@news_blu.route("/news/comment", methods=["POST"])
def news_comment():
    # 提取需要的数据
    news_id = request.json.get("news_id")
    parent_id = request.json.get("parent_id")
    content = request.json.get("content")
    user_id = session.get("user_id")

    # 创建一个Comment对象
    new_comment = Comment()
    new_comment.user_id = user_id
    new_comment.news_id = news_id
    new_comment.content = content
    new_comment.parent_id = parent_id

    db.session.add(new_comment)
    db.session.commit()

    ret = {
        "errno": 0,
        "errmsg": "成功"
    }
    return jsonify(ret)
