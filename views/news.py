from flask import jsonify, request, session

from models import db
from models.index import User, Collection, Comment
from . import news_blu


@news_blu.route("/collect", methods=["POST"])
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


@news_blu.route("/comment", methods=["POST"])
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

    # 3. 根据是否有parent_id来区分是评论还是回复
    if not parent_id:
        # 3.1 评论
        ret = {
            "errno": 0,
            "errmsg": "成功"
        }
        return jsonify(ret)
    else:
        # 3.2 回复
        user = db.session.query(User).filter(User.id == user_id).first()
        parent_comment = db.session.query(Comment).filter(Comment.id == parent_id).first()
        parent_user = parent_comment.user  # 评论的用户
        ret = {
            "errno": 0,
            "errmsg": "成功",
            "comment": {
                "content": content,
                "user": {
                    "avatar_url": user.avatar_url,
                    "nick_name": user.nick_name,
                },
                "parent": {
                    "user": {
                        "nick_name": parent_user.nick_name,
                    },
                    "content": parent_comment.content
                },
                "create_time": new_comment.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "id": new_comment.id,
                "news_id": news_id
            }
        }

        return jsonify(ret)
