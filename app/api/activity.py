from flask import jsonify, json, request, current_app, url_for, make_response
from . import api
from ..models import Journey, Activity
from .util import message_json
from .. import db


@api.route('/activity/<int:aid>')
def get_activity(aid):
    activity = Activity.query.get_or_404(aid)
    return jsonify(activity.to_json())


# 删除
@api.route('/activity/<int:aid>/delete')
def get_activity(aid):
    activity = Activity.query.get_or_404(aid)
    db.session.delete(activity)
    db.session.commit()
    return jsonify(message_json('delete succeed'))


"""
这个单独的方法暂时可能用不到，因为活动的添加都是在行程中进行的
"""
# 添加
@api.route('/activity/new', methods=['POST'])
def create_activity():
    json_data = request.get_json()
    # 没有传送数据的情况
    if json_data is None:
        return message_json('data required')

    data = json.loads(json_data)
    activity = Activity(name=data['name'],
                        journey_id=data['journey_id'],
                        title=data['title'],
                        description=data['description'],
                        order=data['order'],
                        location=data['location'],
                        start_time=data['start_time'],
                        end_time=data['end_time'],
                        )
    db.add(activity)
    db.session.commit()
    return jsonify(activity.to_json())


# TODO 图片处理， 跟新时需要用到
@api.route('/activity/<int:aid>/update-image')
def update_activity(aid):
    pass


#: 跟新活动信息
#: 客户端发送跟新时需要把其他没有更改的参数也发送过来
@api.route('/activity/<int:aid>/update')
def update_activity(aid):
    activity = Activity.query.get_or_404(aid)
    json_data = request.get_json()
    # 没有传送数据的情况
    if json_data is None:
        return message_json('data required')

    data = json.loads(json_data)
    activity['name']=data['name']
    activity['title'] = data['title']
    activity['description'] = data['description']
    activity['location'] = data['location']
    activity['start_time'] = data['start_time']
    activity['end_time'] = data['end_time']

    db.add(activity)
    db.session.commit()
    return jsonify(activity.to_json())
