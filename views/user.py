from flask import jsonify, request, session, render_template

from models import db
from models.index import Follow, User
from . import user_blu


@user_blu.route("/user/follow", methods=["POST"])
def follow():
    # 提取这个请求的目的是，关注还是取消关注
    action = request.json.get("action")
    # 从用户提交的数据中取出作者的id
    news_author_id = request.json.get("user_id")  # 作者的id
    # 从session中取出当前用户的id
    user_id = session.get("user_id")  # 当前用户的id

    if action == "do":
        # 实现关注的大体逻辑

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

    elif action == "undo":

        follow = db.session.query(Follow).filter(Follow.followed_id == news_author_id, Follow.follower_id == user_id).first()
        db.session.delete(follow)
        db.session.commit()

        ret = {
            "errno": 0,
            "errmsg": "取消关注成功"
        }

        return jsonify(ret)


@user_blu.route("/user/user_center")
def user_center():
    return render_template("user.html")


@user_blu.route("/user/user_base_info.html")
def user_base_info():
    return render_template("user_base_info.html")


@user_blu.route("/user/basic", methods=["POST"])
def user_basic():
    # 1. 取参数
    nick_name = request.json.get("nick_name")
    signature = request.json.get("signature")
    gender = request.json.get("gender")

    # 2. 查询用户
    user_id = session.get("user_id")
    user = db.session.query(User).filter(User.id == user_id).first()
    if user:
        # 有这个用户
        # 3.修改用户数据
        user.nick_name = nick_name
        user.signature = signature
        user.gender = gender
        # 4. 保存数据
        db.session.commit()
        ret = {
            "errno": 0,
            "errmsg": "成功"
        }
    else:
        # 没有这个用户
        ret = {
            "errno": 4001,
            "errmsg": "修改失败"
        }

    # 5. 返回操作结果信息
    return jsonify(ret)


@user_blu.route("/user/user_pass_info.html")
def user_pass_info():
    return render_template("user_pass_info.html")


@user_blu.route("/user/password", methods=["POST"])
def user_password():
    # 1. 取数据
    # old_password = request.json.get("old_password")
    new_password = request.json.get("new_password")

    print("--------1--------")

    # 2. 查询用户
    user_id = session.get("user_id")
    user = db.session.query(User).filter(User.id == user_id).first()
    if user:
        # 有这个用户
        # 3.修改用户数据
        print("--------2--------")
        print(user)
        print(new_password)
        user.password_hash = new_password
        print("--------2-0-------")
        # 4. 保存数据
        db.session.commit()
        print("--------2-1-------")
        ret = {
            "errno": 0,
            "errmsg": "成功"
        }
    else:
        # 没有这个用户
        ret = {
            "errno": 4002,
            "errmsg": "修改失败"
        }

    print("--------3--------")

    # 5. 返回对应数据
    return jsonify(ret)
