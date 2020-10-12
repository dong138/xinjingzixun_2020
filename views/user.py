import hashlib
import time

from flask import jsonify, request, session, render_template, url_for, redirect

from models import db
from models.index import Follow, User, Category, News
from utils.image_qiniu import upload_image_to_qiniu
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
    user_id = session.get("user_id")
    user = db.session.query(User).filter(User.id == user_id).first()
    return render_template("index/user.html", user=user)


@user_blu.route("/user/user_base_info.html")
def user_base_info():
    return render_template("index/user_base_info.html")


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
    return render_template("index/user_pass_info.html")


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


@user_blu.route("/user/user_pic_info.html")
def user_pic_info():
    user_id = session.get("user_id")
    user = db.session.query(User).filter(User.id == user_id).first()
    return render_template("index/user_pic_info.html", user=user)


@user_blu.route("/user/avatar", methods=["POST"])
def user_avatar():
    # 1. 提取用户上传的图片
    # request.args.get()
    # request.form.get()
    # request.json.get()
    f = request.files.get("avatar")
    if not f:
        return jsonify({
            "errno": 4003,
            "errmsg": "失败"
        })

    print('---->', f.filename)

    # h = hashlib.md5()
    # h.update((f.filename + str(time.time())).encode("utf-8"))  # 不同用户上传的文件名可能相同，但是时间点一定不同，此时加密的内容就一定不同，从而一定得到不相同的名字
    # hash_val = h.hexdigest()

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "errno": 4004,
            "errmsg": "未登录..."
        })

    # 2. 将用户上传的图片存储
    new_file_name = str(user_id) + f.filename[f.filename.rfind("."):]
    path_file_name = "./static/upload/%s" % new_file_name
    f.save(path_file_name)

    qiniu_image_url = upload_image_to_qiniu(path_file_name, new_file_name)  # 上传到七牛云服务器

    # 3. 修改数据库中这个用户的头像信息
    user_id = session.get("user_id")
    user = db.session.query(User).filter(User.id == user_id).first()
    user.avatar_url = qiniu_image_url
    db.session.commit()

    # 4. 返回信息给前端
    ret = {
        "errno": 0,
        "errmsg": "上传头像成功"
    }

    return jsonify(ret)


@user_blu.route("/user/user_follow.html")
def user_follow():
    # 提取页数
    page = int(request.args.get("page", 1))
    user_id = session.get("user_id")
    user = db.session.query(User).filter(User.id == user_id).first()
    paginate = user.followers.paginate(page, 2, False)  # 查询当前用户所有的粉丝中的第1页
    return render_template("index/user_follow.html", paginate=paginate)


@user_blu.route("/user/user_collection.html")
def user_collection():
    # 提取页码
    page = int(request.args.get("page", 1))

    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index.index"))

    # 提取当前登录的用户
    user = db.session.query(User).filter(User.id == user_id).first()
    paginate = user.collection_news.paginate(page, 1, False)

    return render_template("index/user_collection.html", paginate=paginate)


@user_blu.route("/user/user_news_release.html")
def user_news_release():
    category = db.session.query(Category).filter(Category.id != 1).all()
    return render_template("index/user_news_release.html", category=category)


@user_blu.route("/user/release", methods=["POST"])
def news_release():
    # 提取数据
    title = request.form.get("title")
    category_id = request.form.get("category_id")
    digest = request.form.get("digest")
    f = request.files.get("index_image_url")
    content = request.form.get("content")

    qiniu_image_url = ""
    if f:
        # 计算一个哈希值
        h = hashlib.md5()
        h.update((f.filename + str(time.time())).encode())
        hash_val = h.hexdigest()

        # 保存用户上传的图片
        new_file_name = hash_val + f.filename[f.filename.rfind("."):]
        path_file_name = "./static/upload/%s" % new_file_name
        f.save(path_file_name)

        # 将图片上传到七牛云服务器
        qiniu_image_url = upload_image_to_qiniu(path_file_name, new_file_name)  # 上传到七牛云服务器

    # 简单验证数据
    print(title, category_id, digest, f, content)

    # 创建一个新闻对象（模型类对象），添加到数据库
    news = News()
    news.title = title
    news.source = "xxx网站"
    news.digest = digest
    news.content = content
    news.index_image_url = qiniu_image_url
    news.status = 1
    news.user_id = session.get("user_id")
    news.category_id = int(category_id)

    db.session.add(news)
    db.session.commit()

    ret = {
        "errno": 0,
        "errmsg": "成功"
    }
    return jsonify(ret)


@user_blu.route("/user/user_news_list.html")
def user_news_list():
    # 获取页码
    page = int(request.args.get("page", 1))
    # 查询当前用户
    user_id = session.get("user_id")
    user = db.session.query(User).filter(User.id == user_id).first()

    # 查询当前用户的所有的新闻
    news_paginate = user.news.paginate(page, 1, False)

    return render_template("index/user_news_list.html", news_paginate=news_paginate)
