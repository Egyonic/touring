from flask import jsonify, json, request, current_app, url_for, make_response
from . import api
from ..models import Journey, Activity
from .util import message_json
from .. import db
from datetime import datetime
from dateutil import parser as time_parser


@api.route('/activity/<int:aid>')
def get_activity(aid):
    activity = Activity.query.get_or_404(aid)
    return jsonify(activity.to_json())


# 删除
@api.route('/activity/<int:aid>/delete')
def delete_activity(aid):
    activity = Activity.query.get_or_404(aid)
    db.session.delete(activity)
    db.session.commit()
    return jsonify(message_json('delete succeed'))


# 添加
@api.route('/activity/new', methods=['POST'])
def create_activity():
    json_data = request.get_json()
    # 没有传送数据的情况
    if json_data is None:
        return message_json('data required')

    data = json.loads(json_data)
    t1 = time_parser.parse(data['start_time'])
    t2 = time_parser.parse(data['end_time'])
    activity = Activity(
                        journey_id=data['journey_id'],
                        title=data['title'],
                        description=data['description'],
                        order=data['order'],
                        location=data['location'],
                        start_time=t1,
                        end_time=t2,
                        )
    db.session.add(activity)
    db.session.commit()
    return jsonify(activity.to_json())


# TODO 图片处理， 跟新时需要用到
@api.route('/activity/<int:aid>/update-image')
def update_activity_image(aid):
    pass


#: 跟新活动信息
#: 客户端发送跟新时需要把其他没有更改的参数也发送过来
@api.route('/activity/<int:aid>/update', methods=['POST'])
def update_activity(aid):
    activity = Activity.query.get_or_404(aid)
    json_data = request.get_json()
    # 没有传送数据的情况
    if json_data is None:
        return message_json('data required')

    data = json.loads(json_data)
    t1 = time_parser.parse(data['start_time'])
    t2 = time_parser.parse(data['end_time'])

    activity.title = data['title']
    activity.description = data['description']
    activity.location = data['location']
    activity.start_time = t1
    activity.end_time = t2
    activity.last_modify = datetime.now()

    db.session.add(activity)
    db.session.commit()
    return jsonify(activity.to_json())
