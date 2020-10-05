from flask import jsonify

from . import news_blu


@news_blu.route("/news/collect", methods=["POST"])
def news_collect():
    ret = {
        "errno": 0,
        "errmsg": "成功"
    }

    return jsonify(ret)
