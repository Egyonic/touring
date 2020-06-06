from flask import jsonify, json, request,logging ,url_for, make_response, current_app
from . import api
from datetime import datetime,timedelta
from ..models import User, Journey,user_journey, Activity,Label, BillInfo
from .util import message_json
from .. import db
from dateutil import parser as time_parser
from random import randint


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
    # json_data = request.get_json()
    # # 没有传送数据的情况
    # # logger1.info('------json data ------\n' + json.dumps(json_data))
    # if json_data is None:
    #     return message_json('data required')
    #
    # data = json.loads(json_data)
    if request.data is None:
        return jsonify({'message': 'data required'})
    data = json.loads(request.data)

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
    # json_data = request.get_json()
    # # 没有传送数据的情况
    # if json_data is None:
    #     return message_json('data required')

    # data = json.loads(json_data)
    if request.data is None:
        return jsonify({'message': 'data required'})
    data = json.loads(request.data)

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
    # json_data = request.get_json()
    # # 没有传送数据的情况
    # if json_data is None:
    #     return message_json('data required')
    #
    # data = json.loads(json_data)

    if request.data is None:
        return jsonify({'message': 'data required'})
    data = json.loads(request.data)
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
    # json_data = request.get_json()
    # # 没有传送数据的情况
    # if json_data is None:
    #     return message_json('data required')
    #
    # data = json.loads(json_data)
    if request.data is None:
        return jsonify({'message': 'data required'})
    data = json.loads(request.data)

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


# 按日期分列表项返回活动信息
@api.route('/journey/<int:jid>/activity-by-date', methods=['GET'])
def journey_get_activity_by_date(jid):
    journey = Journey.query.get_or_404(jid)
    logger = logging.create_logger(current_app)
    # 获取所有活动
    activities = journey.activities
    if activities is None or len(activities) == 0:
        return jsonify({
            'activities': [],
            'count': 0
        })

    # 按开始日期排序后的列表
    activities_by_date = sorted(activities,key=lambda x:x.start_time)
    t_date = datetime(year=2000,month=1, day=1, hour=1,minute=1,second=1) # 初始化用于比较的日期
    #t_date = activities[0].start_time # 初始化用于比较的日期
    #t_date = t_date - timedelta(days=3)
    items = []
    for activity in activities_by_date:
        # 如果没有出现过这个日期，创建一个新的对象
        logger.info(f't_date.date type:{type(t_date)}')
        if activity.start_time.date() != t_date.date():
            logger.info(f'日期为{activity.start_time.date()}')
            item = {
                "date": f'{activity.start_time.date()}',
                "activity": [activity.to_json()]
            }
            items.append(item)
            logger.info(f'创建,添加了活动，日期为{activity.start_time.date()}')
            # 跟新上次日期
            t_date = activity.start_time
        else:
            for i in items:
                # 寻找日期相同的组，加入其中
                if i['date'] == f'{activity.start_time.date()}':
                    i['activity'].append(activity.to_json())
                    logger.info(f'添加了活动，日期为{activity.start_time.date()}')

    return jsonify({
        'data': items,
        'days': len(items)
    })


# 随机获取一些行程，用于模拟发现，推荐等
# count 参数指定要获取的数量
@api.route('/journey/explore/<int:count>', methods=['GET'])
def journey_get_random(count):
    journeys = Journey.query.all()
    length = len(journeys)

    # 检查数量是否有效
    data = []
    if 0 < count <= length:
        for i in range(0,count):
            index = randint(0, length - 1)
            data.append(journeys[index].to_json())
        return jsonify({
            "data": data,
            "count": count
        })
    else:
        return jsonify({
            "message": "count is out of the limit"
        })




