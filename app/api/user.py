from flask import jsonify, json, request, current_app, url_for, make_response
from . import api
from ..models import User, Journey,Activity, Label,BillItem, BillInfo, Share
from datetime import datetime
from .util import message_json
from .. import db

# 通过id返回用户信息
@api.route('/users/<int:uid>')
def get_user_info(uid):
    user = User.query.get_or_404(uid)
    return jsonify(user.to_json())


# 创建
@api.route('/users/new', methods=['POST'])
def create_user():
    # json_data = request.get_json()
    # # 没有传送数据的情况
    # if json_data is None:
    #     return message_json('data required')

    if request.data is None:
        return jsonify({'message': 'data required'})
    data = json.loads(request.data)

    user = User(name=data['name'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json())


# 通过name返回用户信息
@api.route('/users/<string:name>')
def get_user_info_by_name(name):
    # 确定用户存在
    user = User.query.get_or_404(name=name)
    return jsonify(user.to_json())


# 获取用户的所有行程
@api.route('/users/<int:uid>/journeys')
def get_user_all_journeys(uid):
    user = User.query.get_or_404(uid)
    journeys = user.journeys
    # 无数据时的情况
    if(journeys is None) or (len(journeys) == 0):
        return jsonify({
            'journeys': [],
            'count': 0
        })
    # 正常返回数据
    return jsonify({
         'journeys': [j.to_json() for j in journeys],
         'count': len(journeys)
    })


# 获取用户已经结束的行程
@api.route('/users/<int:uid>/past-journeys')
def get_user_past_journeys(uid):
    user = User.query.get_or_404(uid)
    journeys = user.journeys
    # 长度为0处理
    if (journeys is None) or (len(journeys) == 0):
        return jsonify({
            'journeys': [],
            'count': 0
        })
    # 筛选
    journey_arr = []
    for j in journeys:
        if j.end_time < datetime.now():
            journey_arr += j
    return jsonify({
        'journeys': [j.to_json() for j in journey_arr],
        'count': len(journey_arr)
    })


# 获取用户未开始的行程
@api.route('/users/<int:uid>/later-journeys')
def get_user_later_journeys(uid):
    user = User.query.get_or_404(uid)
    journeys = user.journeys
    # 长度为0处理
    if (journeys is None) or (len(journeys) == 0):
        return jsonify({
            'journeys': [],
            'count': 0
        })
    # 筛选
    journey_arr = []
    for j in journeys:
        if j.start_time > datetime.now():
            journey_arr += j
    return jsonify({
        'journeys': [j.to_json() for j in journey_arr],
        'count': len(journey_arr)
    })


# 获取用户正在进行的行程
@api.route('/users/<int:uid>/present-journeys')
def get_user_present_journeys(uid):
    user = User.query.get_or_404(uid)
    journeys = user.journeys
    # 长度为0处理
    if (journeys is None) or (len(journeys) == 0):
        return jsonify({
            'journeys': [],
            'count': 0
        })
    # 筛选
    journey_arr = []
    for j in journeys:
        if j.start_time < datetime.now() < j.end_time:
            journey_arr += j
    return jsonify({
        'journeys': [j.to_json() for j in journey_arr],
        'count': len(journey_arr)
    })
