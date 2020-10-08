from flask import jsonify, request, session

from models import db
from models.index import User, Collection, Comment
from . import news_blu


@news_blu.route("/news/collect", methods=["POST"])
def news_collect():
    # 1. 提取参数
    news_id = request.json.get("news_id")
    action = request.json.get("action")  # do表示关注 undo表示取消关注

    # 2. 获取当前用户的id
    user_id = session.get("user_id")

    # 3. 如果是关注功能
    if action == "do":
        collection = Collection()
        collection.news_id = news_id
        collection.user_id = user_id
        try:
            db.session.add(collection)
            db.session.commit()
            ret = {
                "errno": 0,
                "errmsg": "成功"
            }
        except Exception as ret:
            ret = {
                "errno": 5001,
                "errmsg": "关注失败..."
            }

    elif action == "undo":
        collection = db.session.query(Collection).filter(Collection.user_id == user_id, Collection.news_id == news_id).first()
        if collection:
            db.session.delete(collection)
            db.session.commit()
            ret = {
                "errno": 0,
                "errmsg": "取消收藏成功"
            }
        else:
            ret = {
                "errno": 5002,
                "errmsg": "取消收藏失败"
            }

    return jsonify(ret)


@news_blu.route("/news/comment", methods=["POST"])
def news_comment():
    # 1. 提取出用户评价时的数据
    content = request.json.get("content")
    news_id = request.json.get("news_id")
    parent_id = request.json.get("parent_id")
    user_id = session.get("user_id")

    # 2. 保存到数据库
    new_comment = Comment()
    new_comment.news_id = news_id
    new_comment.user_id = user_id
    new_comment.content = content
    new_comment.parent_id = parent_id
    db.session.add(new_comment)
    db.session.commit()

    ret = {
        "errno": 0,
        "errmsg": "成功"
    }
    return jsonify(ret)
