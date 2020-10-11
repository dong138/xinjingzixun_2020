from flask import render_template

from . import admin_blu


@admin_blu.route("/admin")
def admin():
    return render_template("admin/index.html")
