from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_session import Session

from views import index_blu, passport_blu, user_blu, news_blu, admin_blu
from models import db
from utils.common import show_top_6_news_style, show_news_status_name, show_news_status_style_name, set_after_request_handle_fuc

# 创建flask应用对象
app = Flask(__name__)

# 加载配置
app.config.from_pyfile("config.ini")

# 创建蓝图，且注册到app
app.register_blueprint(index_blu)
app.register_blueprint(passport_blu, url_prefix="/passport")
app.register_blueprint(user_blu, url_prefix="/user")
app.register_blueprint(news_blu, url_prefix="/news")
app.register_blueprint(admin_blu, url_prefix="/admin")

# 初始化数据库
db.init_app(app)

# 创建Session对象（此时app这个flask对象中生成的session信息才会存储到Redis里）
Session(app)

# 添加过滤器
app.add_template_filter(show_top_6_news_style)
app.add_template_filter(show_news_status_name)
app.add_template_filter(show_news_status_style_name)

# 设置钩子函数，可以在调用视图函数之前自动执行
set_after_request_handle_fuc(app)

# 添加数据库迁移等工具
manager = Manager(app)
# 生成migrate对象 用来数据库迁移
migrate = Migrate(app, db)
# 添加db命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # app.run(port=8899)
    manager.run()
