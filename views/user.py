from flask import jsonify, request, session

from models import db
from models.index import Follow
from . import user_blu


@user_blu.route("/user/follow", methods=["POST"])
def follow():
    # 实现关注的大体逻辑
    # 从用户提交的数据中取出作者的id
    action = request.json.get("action")
    news_author_id = request.json.get("user_id")  # 作者的id

    # 从session中取出当前用户的id
    user_id = session.get("user_id")  # 当前用户的id

    # 创建SQLAlchemy对象
    follow = Follow(followed_id=news_author_id, follower_id=user_id)

    # 最终像follow数据表中添加一行记录
    db.session.add(follow)
    db.session.commit()

    ret = {
        "errno": 0,
        "errmsg": "关注成功..."
    }
    return jsonify(ret)
