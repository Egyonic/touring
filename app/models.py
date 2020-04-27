from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from . import db


user_journey = db.Table('user_journey',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('journey_id', db.Integer, db.ForeignKey('journey.id'), primary_key=True)
    )


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True, default="null")
    password_hash = db.Column(db.String(128))
    # password = db.Column(db.String(20))
    confirmed = db.Column(db.Boolean, default=False)

    # 关系定义
    bill_infos = db.relationship('BillInfo', lazy='select',
                                 backref=db.backref('owner', lazy='joined'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        json_user = {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
        return json_user

    def verify_password(self, password):
        return password == self.password

    def generate_auth_token(self, expiration):
        pass

    @staticmethod
    def verify_auth_token(token):
        pass

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class Label(db.Model):
    """标签表
    用于方便的更改账单信息表中的标签，通过更改label表中的name属性来修改内容
    """
    __tablename__ = 'label'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)

    def __init__(self, **kwargs):
        super(Label, self).__init__(**kwargs)


class BillInfo(db.Model):
    """ 账单信息表
    owner: 所有者用户id
    count: 参与的人数
    """
    __tablename__ = 'bill_info'
    id = db.Column(db.Integer, primary_key=True)
    journey_id = db.Column(db.Integer, db.ForeignKey('journey.id'),  nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    description = db.Column(db.String(100), nullable=True)
    label_id = db.Column(db.Integer, db.ForeignKey('label.id'))
    cost = db.Column(db.REAL, nullable=True)
    count = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.Integer)

    # 关系定义
    owner = db.relationship('User', lazy=True, uselist=False)
    label = db.relationship('Label', lazy=True, uselist=False)
    journey = db.relationship('Journey', lazy=True, uselist=False)
    #  属于该账单信息的所有账单项
    items = db.relationship('BillItem', lazy=True,
                            backref=db.backref('bill_info', lazy=True))

    def to_json(self):
        pass

    def get_status_list(self):
        pass

    def __init__(self, **kwargs):
        super(BillInfo, self).__init__(**kwargs)


class BillItem(db.Model):
    __tablename__ = 'bill_item'
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill_info.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # status 0为未结算 1为已付款
    status = db.Column(db.Integer, default=False)

    def get_status_list(self):
        pass

    def __init__(self, **kwargs):
        super(BillItem, self).__init__(**kwargs)


class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True)
    journey_id = db.Column(db.Integer, db.ForeignKey('user.id'), )
    title = db.Column(db.String(30), nullable=True)
    description = db.Column(db.String(100))
    order = db.Column(db.Integer, default=1)
    location = db.Column(db.String(50))
    # 图片保存位置
    image = db.Column(db.String(100))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    last_modify = db.Column(db.DateTime)

    def update_last(self):
        pass

    def to_json(self):
        pass

    def __init__(self, **kwargs):
        super(Activity, self).__init__(**kwargs)


class Journey(db.Model):
    __tablename__ = 'journey'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    destination = db.Column(db.String(50))
    start_time = db.Column(db.DateTime, default=datetime.now())
    end_time = db.Column(db.DateTime, default=datetime.now() + datetime.day)
    budget = db.Column(db.REAL)
    cover = db.Column(db.String(100))
    status = db.Column(db.Integer)

    # 关系定义
    owner = db.relationship('User', lazy=True, uselist=False)
    # 该行程的所有成员
    members = db.relationship('User', secondary=user_journey, lazy=True,
                              backref=db.backref('journeys', lazy=True))

    def to_json(self):
        pass

    def get_journey_item(self):
        pass

    def total_cost(self):
        pass

    def __init__(self, **kwargs):
        super(Journey, self).__init__(**kwargs)


class Share(db.Model):
    __tablename__ = 'share'
    id = db.Column(db.Integer, primary_key=True)
    journey_id = db.Column(db.Integer, db.ForeignKey('journey.id'), nullable=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    cost = db.Column(db.REAL)
    image = db.Column(db.String(100))
    price = db.Column(db.REAL, default=0.0)
    description = db.Column(db.String(100))
    date = db.Column(db.DateTime)

    def to_json(self):
        pass

    def get_share_itme(self):
        pass

    def __init__(self, **kwargs):
        super(Share, self).__init__(**kwargs)
