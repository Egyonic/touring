import unittest
from faker import Faker
from flask import current_app, logging
from app import create_app, db
from app.models import User, Journey


class UserModelCase(unittest.TestCase):
    """用户模型相关测试

    setUp 会在每个测试测试函数前执行一次
    tearDown 则在每个测试函数结束后执行
    """
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        # 设置app context
        self.app_context.push()
        db.create_all()
        # 设置日志记录器
        self.logger = logging.create_logger(self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_register(self):
        u = User(name="Fear",password='password')
        db.session.add(u)
        self.logger.info(f'user {u.name} had added')

    def test_password_setter(self):
        u = User(name="Fear",password='password')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(name="Fear",password='password')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(name="Fear", password='password')
        self.assertTrue(u.verify_password('password'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        """验证两个相同的密码得出的hash是否一致"""
        u = User(name="Fear",password='password')
        u2 = User(name="Mike",password='password')
        self.assertTrue(u.password_hash != u2.password_hash)