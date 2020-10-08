from datetime import datetime

from . import db


class News(db.Model):
    """新闻"""
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)  # 新闻编号
    title = db.Column(db.String(256), nullable=False)  # 新闻标题
    source = db.Column(db.String(64), nullable=False)  # 新闻来源
    digest = db.Column(db.String(512), nullable=False)  # 新闻摘要
    content = db.Column(db.Text, nullable=False)  # 新闻内容
    clicks = db.Column(db.Integer, default=0)  # 浏览量
    index_image_url = db.Column(db.String(256))  # 新闻列表图片路径
    status = db.Column(db.Integer, default=0)  # 当前新闻状态 如果为0代表审核通过，1代表审核中，-1代表审核不通过
    reason = db.Column(db.String(256))  # 未通过原因，status = -1 的时候使用
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 当前新闻的作者id
    user = db.relationship('User', backref=db.backref('news', lazy='dynamic'))

    category = db.relationship('Category', backref='news')
    # 当前新闻的所有评论
    comments = db.relationship("Comment", lazy="dynamic")

    def to_dict(self):
        """
        定义一个方法，用来将将对象中的部分属性，转换为字典
        :return: 一个字典
        """
        ret = {
            "id": self.id,
            "create_time": self.create_time,
            "digest": self.digest,
            "index_image_url": self.index_image_url,
            "source": self.source,
            "title": self.title
        }
        return ret


class Category(db.Model):
    """新闻分类"""
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    name = db.Column(db.String(64), nullable=False)  # 分类名
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


# 因为User表中用到了Follw，所以就放到前面
class Follow(db.Model):
    """用关注表"""
    __tablename__ = "follow"
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # 被关注人的id
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # 被粉丝id


class Collection(db.Model):
    __tablename__ = "collection"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)  # 新闻编号
    news_id = db.Column(db.Integer, db.ForeignKey("news.id"), primary_key=True)  # 分类编号
    create_time = db.Column(db.DateTime, default=datetime.now)  # 收藏创建时间


class User(db.Model):
    """用户"""
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    avatar_url = db.Column(db.String(256))  # 用户头像路径
    create_time = db.Column(db.DateTime, default=datetime.now)  # 注册时间
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False)
    signature = db.Column(db.String(512))  # 用户签名
    gender = db.Column(  # 性别
        db.Enum(
            "MAN",  # 男
            "WOMAN"  # 女
        ),
        default="MAN"
    )
    followers = db.relationship('User',
                                secondary=Follow.__tablename__,
                                primaryjoin=(id == Follow.followed_id),
                                secondaryjoin=(id == Follow.follower_id),
                                backref=db.backref('followed', lazy='dynamic'),
                                lazy='dynamic')

    collection_news = db.relationship("News",
                                      secondary=Collection.__table__,
                                      backref=db.backref('collected_user', lazy='dynamic'),
                                      lazy='dynamic')


class Comment(db.Model):
    """评论"""
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 评论编号
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # 用户id
    news_id = db.Column(db.Integer, db.ForeignKey("news.id"), nullable=False)  # 新闻id
    content = db.Column(db.Text, nullable=False)  # 评论内容
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now)  # 记录的更新时间
