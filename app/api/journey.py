from flask import jsonify, json, request,logging ,url_for, make_response, current_app
from . import api
from ..models import User, Journey,user_journey, Activity,Label, BillInfo
from .util import message_json
from .. import db
from dateutil import parser as time_parser


@api.route('/journeys/<int:jid>')
def get_journey_info(jid):
    journey = Journey.query.get_or_404(jid)
    return jsonify(journey.to_json())


# 获取行程的所有成员信息
@api.route('/journeys/<int:jid>/members')
def get_journey_members(jid):
    journey = Journey.query.get_or_404(jid)
    members = journey.members
    if members is None or len(members==0):
        return jsonify({
            'members': [],
            'count': 0
        })
    return jsonify({
        'members': [m.to_json() for m in members],
        'count': len(members)
    })


# 返回创建者信息
@api.route('/journeys/<int:jid>/owner')
def get_journey_owner(jid):
    journey = Journey.query.get_or_404(jid)
    return jsonify(journey.owner.to_json())


# 返回行程所有账单
@api.route('/journeys/<int:jid>/billinfos')
def get_journey_bill_infos(jid):
    journey = Journey.query.get_or_404(jid)
    billinfos = journey.billinfos
    # 没有数据的情况
    if billinfos is None or len(billinfos)==0:
        return jsonify({
            'billinfos': [],
            'count': 0
        })

    return jsonify({
        'billinfos': [info.to_json() for info in billinfos],
        'count': 0
    })


# 获取行程的所有活动
@api.route('/journeys/<int:jid>/activities')
def get_journey_activities(jid):
    journey = Journey.query.get_or_404(jid)
    activities = journey.activities
    if activities is None or len(activities)==0:
        return jsonify({
            'activities': [],
            'count': 0
        })

    return jsonify({
        'actitivies': [a.to_json() for a in activities],
        'count': len(activities)
    })


# 通过Jsons数据创建一个行程
@api.route('/journeys/new', methods=['POST'])
def create_journey():
    logger1 = logging.create_logger(current_app)
    json_data = request.get_json()
    # 没有传送数据的情况
    # logger1.info('------json data ------\n' + json.dumps(json_data))
    if json_data is None:
        return message_json('data required')

    data = json.loads(json_data)
    if data['start_time'] is None or data['end_time'] is None:
        return message_json('data required')
    # 客户端在传值时必须给时间，不然是无法创建的
    t1 = time_parser.parse(data['start_time'])
    t2 = time_parser.parse(data['end_time'])
    journey = Journey(name=data['name'],
                      owner_id=data['owner_id'],
                      destination=data['destination'],
                      start_time=t1,
                      end_time=t2,
                      budget=data['budget'],

                      )
    # 获取创建者用户对象
    owner = User.query.get(journey.owner_id)
    db.session.add(journey)
    # 将创建者加入该行程的成员中
    # logger1.info(f'创建者:\n{owner.name}')
    journey.members += [owner]
    db.session.commit()
    return jsonify(journey.to_json())


# 修改行程信息
@api.route('/journeys/<int:jid>update', methods=['POST'])
def update_journey_activity(jid):
    journey = Journey.query.get_or_404(jid)
    json_data = request.get_json()
    # 没有传送数据的情况
    if json_data is None:
        return message_json('data required')

    data = json.loads(json_data)
    journey['name']=data['name']
    journey['owner_id']=data['owner_id'],
    journey['destination']=data['destination'],
    journey['start_time']=data['start_time'],
    journey['end_time']=data['end_time'],
    journey['budget']=data['budget'],
    # 提交修改
    db.session.add(journey)
    db.session.commit()
    return jsonify(journey.to_json())


# TODO 创建行程时的图片上传处理
@api.route('journey/<int:jid>/img-upload', methods=['POST'])
def img_upload(jid):
    journey = Journey.query.get_or_404(jid)



# 添加成员
@api.route('/journey/<int:jid>/add-member', methods=['POST'])
def journey_add_member(jid):
    journey = Journey.query.get_or_404(jid)
    json_data = request.get_json()
    # 没有传送数据的情况
    if json_data is None:
        return message_json('data required')

    data = json.loads(json_data)
    # user 是一个列表，所有要加入行程的用户的id
    users = data['members']
    for u in users:
        user = User.query.get_or_404(u)
        journey.members += [user]
    db.session.commit()
    return message_json('succeed')


# TODO 待测试
# 删除成员
@api.route('/journey/<int:jid>/delete-member', methods=['POST'])
def journey_delete_member(jid):
    journey = Journey.query.get_or_404(jid)
    json_data = request.get_json()
    # 没有传送数据的情况
    if json_data is None:
        return message_json('data required')

    data = json.loads(json_data)
    # user 是一个列表，所有要加入行程的用户的id
    user_id = data['user_id']

    if user_id is not None:
        u = User.query.get(user_id)
        journey.members.remove(u)
        db.session.commit()
    return message_json('succeed')


""" 这个方法暂时不需要，使用activity中的方法来实现
# 为行程添加活动
@api.route('/journey/<int:jid>/add-activity', methods=['POST'])
def journey_add_activity(jid):
    journey = Journey.query.get_or_404(jid)
    json_data = request.get_json()
    # 没有传送数据的情况
    if json_data is None:
        return message_json('data required')

    data = json.loads(json_data)
    activity = Activity(name=data['name'],
                        journey_id=jid,
                        title=data['title'],
                        description=data['description'],
                        order=data['order'],
                        location=data['location'],
                        start_time=data['start_time'],
                        end_time=data['end_time'],
                      )
    db.session.add(activity)
    db.session.commit()
    return jsonify(activity.to_json())

"""
