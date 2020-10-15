import random

from flask import request, jsonify, session, redirect, url_for, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from models import db
from models.index import User
from utils.sms_aliyun import send_msg_to_phone

from . import passport_blu


@passport_blu.route("/register", methods=["GET", "POST"])
def register():
    # 1. 提取数据
    mobile = request.json.get("mobile")
    password = request.json.get("password")
    image_code = request.json.get("image_code")
    smscode = request.json.get("smscode")

    # 2. 测试数据
    print(mobile, password, image_code, smscode)

    # 图片验证码已经在发送短信时使用了，此时就没有必要再校验了，也就是图片验证码是防止过于频繁的发送短信验证码，而短信验证码时防止过于频繁的注册
    # # 验证图片验证码是否争取
    # if session.get("image_code") != image_code:
    #     ret = {
    #         "errno": 1003,
    #         "errmsg": "重新输入验证码"
    #     }
    #     return jsonify(ret)

    # 校验"图片验证码"是否正确
    if session.get("sms_code") != smscode:
        ret = {
            "errno": 1003,
            "errmsg": "重新输入手机验证码"
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
    # user.password_hash = password  # 未加密的方式，这样容易泄露用户名密码
    user.password_hash = generate_password_hash(password)
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


@passport_blu.route("/login", methods=["GET", "POST"])
def login():
    # 1. 提取登录时的用户名，密码
    mobile = request.json.get("mobile")
    password = request.json.get("password")

    # 2. 查询，如果存在表示登录成功，否则失败
    user = db.session.query(User).filter(User.mobile == mobile).first()
    if user and check_password_hash(user.password_hash, password):
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


@passport_blu.route("/logout")
def logout():
    # 清空登录状态
    session.clear()

    return redirect(url_for('index_blu.index'))


@passport_blu.route("/image_code")
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


@passport_blu.route("/smscode", methods=["POST"])
def smscode():
    # 1. 提取数据
    image_code = request.json.get("image_code")
    mobile = request.json.get("mobile")

    # 2. 校验图片验证码是否正确
    image_code_session = session.get("image_code")
    print("输入的验证码", image_code)
    print("生成的验证码", image_code_session)
    if image_code.lower() != image_code_session.lower():
        ret = {
            "errno": 4004,
            "errmsg": "图片验证码错误..."
        }
        return jsonify(ret)

    # 3. 生成一个随机的6位数
    sms_code = str(random.randint(100000, 999999))
    print("短信验证码是:", sms_code)

    # 4. 存储到session中
    session['sms_code'] = sms_code

    # 5. 通过短信发送这个6位数
    # send_msg_to_phone(mobile, sms_code)  # 知道怎样发送短信就行了，我们可以通过print终端打印出验证码 以便测试。当代码开发完毕 放入到生产环境中时  再开启即可

    ret = {
        "errno": 0,
        "errmsg": "发送短信验证码成功..."
    }

    return jsonify(ret)
