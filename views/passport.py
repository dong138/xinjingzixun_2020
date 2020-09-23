from flask import request, jsonify, session, redirect, url_for, make_response

from models import db
from models.index import User

from . import passport_blu


@passport_blu.route("/passport/register", methods=["GET", "POST"])
def register():
    # 1. 提取数据
    mobile = request.json.get("mobile")
    password = request.json.get("password")
    image_code = request.json.get("image_code")
    smscode = request.json.get("smscode")

    # 2. 测试数据
    print(mobile, password, image_code, smscode)

    # 验证图片验证码是否争取
    if session.get("image_code") != image_code:
        ret = {
            "errno": 1003,
            "errmsg": "重新输入验证码"
        }
        return jsonify(ret)

    # 2. 创建一个新的用户
    # 2.1 先查询是否有这个相同的用户
    if db.session.query(User).filter(User.mobile == mobile).first():
        return jsonify({
            "errno": 1001,
            "errmsg": "已经注册..."
        })

    # 2.2 注册用户
    # 将新用户的数据插入到数据库
    user = User()
    user.nick_name = mobile
    user.password_hash = password  # 在第2版中会进行更改，到时会变成加密的
    user.mobile = mobile
    try:
        db.session.add(user)
        db.session.commit()

        # 注册成功之后，立刻认为登录成功，也就说需要进行状态保持
        session['user_id'] = user.id
        session['nick_name'] = mobile

        ret = {
            "errno": 0,
            "errmsg": "注册成功..."
        }
    except Exception as ret:
        print("---->", ret)
        db.session.rollback()  # 如果在将用户的信
        ret = {
            "errno": 1002,
            "errmsg": "注册失败..."
        }

    return jsonify(ret)


@passport_blu.route("/passport/login", methods=["GET", "POST"])
def login():
    # 1. 提取登录时的用户名，密码
    mobile = request.json.get("mobile")
    password = request.json.get("password")

    # 2. 查询，如果存在表示登录成功，否则失败
    user = db.session.query(User).filter(User.mobile == mobile, User.password_hash == password).first()
    if user:
        ret = {
            "errno": 0,
            "errmsg": "登录成功"
        }

        session['user_id'] = user.id
        session['nick_name'] = mobile
    else:
        ret = {
            "errno": 2001,
            "errmsg": "用户名或者密码错误"
        }

    return jsonify(ret)


@passport_blu.route("/passport/logout")
def logout():
    # 清空登录状态
    session.clear()

    return redirect(url_for('index_blu.index'))


@passport_blu.route("/passport/image_code")
def image_code():
    # 读取一个图片
    # with open("./yanzhengma.png", "rb") as f:
    #     image = f.read()

    # 真正的生成一张图片数据
    from utils.captcha.captcha import captcha

    # 生成验证码
    # hash值  验证码值  图片内容
    name, text, image = captcha.generate_captcha()

    print("刚刚生成的验证码：", text)

    # 通过session的方式，缓存刚刚生成的验证码，否则注册时不知道刚刚生成的是多少
    session['image_code'] = text

    # 返回响应内容
    resp = make_response(image)

    # 设置内容类型
    resp.headers['Content-Type'] = 'image/png'

    return resp
