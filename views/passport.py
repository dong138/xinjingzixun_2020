from flask import jsonify, request

from . import passport_blu


@passport_blu.route("/passport/register", methods=["GET", "POST"])
def register():
    # 想要实现注册，大体的流程
    # 1. 获取浏览器提交的数据
    # 2. 创建SQLAlchemy对象
    # 3. 保存到数据库
    # 4. 返回响应的json给浏览器

    # 1. 获取参数
    # request.args.get()  # 获取URL中?后面的参数，例如 http://127.0.0.1:5000/login?name=laowang&password=123456
    # request.form.get()  # 获取form表单的数据
    # request.json.get()  # 获取json的数据
    image_code = request.json.get("image_code")
    mobile = request.json.get("mobile")
    password = request.json.get("password")
    smscode = request.json.get("smscode")


    ret = {
        "errno": 1,
        "errmsg": "登录成功..."
    }
    return jsonify(ret)