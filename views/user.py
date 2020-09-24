from flask import jsonify, session

from . import user_blu


@user_blu.route("/user/follow", methods=["POST"])
def follow():
    # 实现关注的流程
    # 1. 提取当前作者的id
    # 2. 提取当前登录用户的id
    # 3. 判断之前是否已经关注过
    # 4. 如果未关注，则进行关注


    ret = {
        "errno": 0,
        "errmsg": "关注成功"
    }

    return jsonify(ret)
