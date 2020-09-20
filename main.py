from flask import Flask

# 创建flask应用对象
app = Flask(__name__)


@app.route("/")
def index():
    return "我是主页..."


if __name__ == '__main__':
    app.run(port=8899)
