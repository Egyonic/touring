"""
身份认证相关的控制
"""

from flask import g, jsonify, request, logging, current_app
from flask_httpauth import HTTPBasicAuth
from ..models import User
from . import api
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()


# 验证身份信息
@auth.verify_password
def verify_password(email_or_token, password):
    logger = logging.create_logger(current_app)
    # logger.debug('request.authorization' + request.authorization.__str__())
    if request.authorization is None or email_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token.lower()).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


# 使api blueprint中的路由都需要认证才能访问
@api.before_request
@auth.login_required
def before_request():
    pass
    # if not g.current_user.is_anonymous:
    #     return forbidden('Unconfirmed account')


# 用户通过这个函数来获取token
@api.route('/tokens/', methods=['POST'])
def get_token():
    if g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})
