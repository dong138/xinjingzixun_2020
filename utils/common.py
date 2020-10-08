def show_clicks_top_6_news(index):
    if index == 1:
        return "first"
    elif index == 2:
        return "second"
    elif index == 3:
        return "third"

    return ""


def show_news_status(index):
    if index == 0:
        return "已通过"
    elif index == 1:
        return "审核中"
    elif index == -1:
        return "未通过"

    return ""


def show_news_status_class_name(index):
    if index == 0:
        return "pass"
    elif index == 1:
        return "review"
    elif index == -1:
        return "nopass"

    return ""
