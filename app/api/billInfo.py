from flask import jsonify, json, request, current_app, url_for, make_response
from . import api
from ..models import Label,BillItem, BillInfo, Journey, User
from .. import db
from .util import message_json


# 获取账单信息的所有记录项
@api.route('/bill_info/<int:bid>')
def get_bill_info(bid):
    bill_info = BillInfo.query.get_or_404(bid)
    return jsonify(bill_info.to_json())


# 获取所有子记录
@api.route('/bill_info/<int:bid>/items')
def get_bill_info_items(bid):
    billinfo = BillInfo.query.get_or_404(bid)
    items = billinfo.items
    if items is None or len(items)==0:
        return jsonify({
            'items': [],
            'count': 0
        })
    return jsonify({
        'items': [item.to_json() for item in items],
        'count': len(items)
    })


# 创建
@api.route('/bill_info/new', methods=['POST'])
def create_bill_info():
    # json_data = request.get_json()
    # # 没有传送数据的情况
    # if json_data is None:
    #     return message_json('data required')
    #
    # data = json.loads(json_data)

    if request.data is None:
        return jsonify({'message': 'data required'})
    data = json.loads(request.data)

    info = BillInfo(journey_id=data['journey_id'],
                    owner_id=data['owner_id'],
                    description=data['description'],
                    label_id=data['label_id'],
                    cost=data['cost'],
                    )
    db.session.add(info)

    # 为行程的所有用户添加记录
    journey = Journey.query.get_or_404(data['journey_id'])
    for user in journey.members:
        item = BillItem(bill_info_id=info.id,
                        user_id=user.id)
        db.session.add(item)
    # count 人数，即为所有成员的数量
    info.count= len(journey.members)
    db.session.commit()
    return jsonify(info.to_json())


#TODO 可以传入 members 信息，即哪些参加的人，来实现为部分人添加
#