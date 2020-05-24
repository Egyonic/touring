from flask import jsonify, json, request, current_app, url_for, make_response
from . import api
from ..models import Label,BillItem, BillInfo
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
@api.route('/bill_info/new')
def create_bill_info():
    json_data = request.get_json()
    # 没有传送数据的情况
    if json_data is None:
        return message_json('data required')

    data = json.loads(json_data)
    info = BillInfo(journey_id=data['journey_id'],
                    owner_id=data['owner_id'],
                    description=data['description'],
                    label_id=data['label_id'],
                    cost=data['cost'],
                    count=data['count']
                    )
    db.session.add(info)
    db.session.commit()
    return jsonify(info.to_json())

