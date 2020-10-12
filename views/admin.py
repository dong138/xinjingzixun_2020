from flask import render_template
from flask import jsonify

from models import db
from models.index import Category
from . import admin_blu


@admin_blu.route("/admin")
def admin():
    return render_template("admin/index.html")


@admin_blu.route("/admin/user_count.html")
def user_count():
    return render_template("admin/user_count.html")


@admin_blu.route("/admin/user_list.html")
def user_list():
    return render_template("admin/user_list.html")


@admin_blu.route("/admin/news_review.html")
def news_review():
    return render_template("admin/news_review.html")


@admin_blu.route("/admin/news_edit.html")
def news_edit():
    return render_template("admin/news_edit.html")


@admin_blu.route("/admin/news_type.html")
def news_type():
    news_types = db.session.query(Category).filter(Category.id != 1).all()
    return render_template("admin/news_type.html", news_types=news_types)


@admin_blu.route("/admin/news_type", methods=["POST"])
def news_type_edit():
    ret = {
        "errno": 0,
        "errmsg": "成功"
    }

    return jsonify(ret)
