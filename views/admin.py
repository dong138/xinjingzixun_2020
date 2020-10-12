from flask import render_template

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
