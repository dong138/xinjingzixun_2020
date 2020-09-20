from flask import Flask

from views import index_blu

# 创建flask应用对象
app = Flask(__name__)

# 创建蓝图，且注册到app
app.register_blueprint(index_blu)

if __name__ == '__main__':
    app.run(port=8899)
