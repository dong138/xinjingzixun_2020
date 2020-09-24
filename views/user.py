from flask import jsonify, session, request

from models import db
from models.index import User, Follow
from . import user_blu


@user_blu.route("/user/follow", methods=["POST"])
def follow():
    action = request.json.get("action")

    if action == "do":
        # 实现关注的流程
        # 1. 提取当前作者的id
        # 2. 提取当前登录用户的id
        # 3. 判断之前是否已经关注过
        # 4. 如果未关注，则进行关注

        # 1. 提取当前作者的id
        news_author_id = request.json.get("user_id")

        # 2. 提取当前登录用户的id
        user_id = session.get("user_id")

        # 3. 判断之前是否已经关注过
        news_author = db.session.query(User).filter(User.id == news_author_id).first()
        if user_id in [x.id for x in news_author.followers]:
            return jsonify({
                "errno": 3001,
                "errmsg": "已经关注了，请勿重复关注..."
            })

        # 4. 如果未关注，则进行关注
        try:
            follow = Follow(followed_id=news_author_id, follower_id=user_id)
            db.session.add(follow)
            db.session.commit()

            ret = {
                "errno": 0,
                "errmsg": "关注成功"
            }

            return jsonify(ret)

        except Exception as ret:
            ret = {
                "errno": 3003,
                "errmsg": "关注失败..."
            }

            return jsonify(ret)

    else:
        # 取消关注
        ret = {
            "error": 0,
            "errmsg": "取消关注成功"
        }

        return jsonify(ret)
