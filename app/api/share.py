from flask import jsonify, json, request, current_app, url_for, make_response
from . import api
from ..models import Share
from .util import message_json
from .. import db
from .util import message_json


# 获取分享信息
@api.route('/share/<int:sid>')
def get_share_info(sid):
    share = Share.query.get_or_404(sid)
    return jsonify(share.to_json())


# 创建
@api.route('/share/new',methods=['POST'])
def create_share():
    # json_data = request.get_json()
    # # 没有传送数据的情况
    # if json_data is None:
    #     return message_json('data required')
    #
    # data = json.loads(json_data)

    if request.data is None:
        return jsonify({'message': 'data required'})
    data = json.loads(request.data)

    share = Share(
        journey_id=data['journey_id'],
        user_id=data['user_id'],
        cost=data['cost'],
        price=data['price'],
        description=data['description'],
    )
    db.session.add(share)
    db.session.commit()
    return jsonify(share.to_json())

# TODO 图片处理