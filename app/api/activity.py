from flask import jsonify, json, request, current_app, url_for, make_response, logging, send_from_directory
from . import api
from ..models import Journey, Activity
from .util import message_json
from .. import db
from datetime import datetime
from dateutil import parser as time_parser
import os
import uuid

# 获取上传文件的接口
@api.route('/uploads/<path:filename>')
def get_upload_file(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'],filename)


@api.route('/activity/<int:aid>')
def get_activity(aid):
    activity = Activity.query.get_or_404(aid)
    return jsonify(activity.to_json())


# 删除
@api.route('/activity/<int:aid>/delete', methods=['POST'])
def delete_activity(aid):
    activity = Activity.query.get_or_404(aid)
    db.session.delete(activity)
    db.session.commit()
    return jsonify(message_json('delete succeed'))


# 添加
@api.route('/activity/new', methods=['POST'])
def create_activity():
    # json_data = request.get_json()
    # # 没有传送数据的情况
    # if json_data is None:
    #     return message_json('data required')
    #
    # data = json.loads(json_data)

    if request.data is None:
        return jsonify({'message': 'data required'})
    data = json.loads(request.data)

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


# 生产新的随机文件名的函数
def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


# TODO 图片处理， 跟新图片时需要用到
@api.route('/activity/<int:aid>/update-image', methods=['POST'])
def update_activity_image(aid):
    activity = Activity.query.get_or_404(aid)
    # logger = logging.create_logger(current_app)
    # logger.info(f'headers:\n{request.headers}')
    file = request.files.get('image')
    if file:
        # 获取新文件名
        new_name = random_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_PATH'],new_name)
        file.save(file_path)
        # 保存图片的信心
        activity.image = f'static/uploads/{new_name}'
        db.session.add(activity)
        db.session.commit()
        return jsonify({
            "message": "success"
        })
    else:
        return jsonify({
            "message": "error"
        })




#: 跟新活动信息
#: 客户端发送跟新时需要把其他没有更改的参数也发送过来
@api.route('/activity/<int:aid>/update', methods=['POST'])
def update_activity(aid):
    activity = Activity.query.get_or_404(aid)
    # json_data = request.get_json()
    # # 没有传送数据的情况
    # if json_data is None:
    #     return message_json('data required')

    # data = json.loads(json_data)

    if request.data is None:
        return jsonify({'message': 'data required'})
    data = json.loads(request.data)

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
