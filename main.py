from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from views import index_blu, passport_blu, user_blu
from models import db
from utils.common import show_clicks_top_6_news

# 创建flask对象
app = Flask(__name__)

# 注册蓝图
app.register_blueprint(index_blu)
app.register_blueprint(passport_blu)
app.register_blueprint(user_blu)

# 配置app
app.config.from_pyfile("config.ini")

# 将SQLAlchemy对象与app对象进行关联，从而让SQLAlchemy对象知道响应的数据库配置
db.init_app(app)

# 添加自定义过滤器
app.add_template_filter(show_clicks_top_6_news)

# 添加数据库迁移等工具
manager = Manager(app)
# 生成migrate对象 用来数据库迁移
migrate = Migrate(app, db)
# 添加db命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # app.run(port=8899)
    manager.run()
