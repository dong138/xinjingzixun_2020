from flask import session, g

from models import db
from models.index import User


def show_top_6_news_style(index):
    if index == 1:
        return "first"
    elif index == 2:
        return "second"
    elif index == 3:
        return "third"
    return ""


def show_news_status_name(index):
    if index == 0:
        return "已通过"
    elif index == 1:
        return "审核中"
    elif index == -1:
        return "未通过"
    return ""


def show_news_status_style_name(index):
    if index == 0:
        return "pass"
    elif index == 1:
        return "review"
    elif index == -1:
        return "nopass"
    return ""


def set_after_request_handle_fuc(app):
    """
    对flask对象 设置 每次调用视图函数之前，要执行的事情
    """

    @app.before_request
    def before_request():
        # 查询当前登录用户，如果未登录那么g.user为None，如果登录了g.user就是当前登录用户对象
        # 之所有用g变量，是因为我们可以把需要给视图函数传递的参数，通过给g对象添加属性的方式让g进行携带
        # 然后在视图函数中就可以通过g.user提取出来。也就是说g能够帮我们在多个函数之间传递参数
        user_id = session.get("user_id")
        g.user = db.session.query(User).filter(User.id == user_id).first()
