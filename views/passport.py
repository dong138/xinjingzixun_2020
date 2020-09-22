from . import passport_blu


@passport_blu.route("/passport/register", methods=["GET", "POST"])
def register():
    return "成功"
