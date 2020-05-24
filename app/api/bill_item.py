from flask import jsonify, json, request, current_app, url_for, make_response
from . import api
from ..models import Label,BillItem, BillInfo
from .. import db
from .util import message_json

# 获取记录信息的\
@api.route('/bill_item/<int:bid>')
def get_bill_item_info(bid):
    bill_info = BillInfo.query.get_or_404(bid)
    return jsonify(bill_info.to_json())


# 创建
@api.route('/bill_item/new')
def create_bill_item():
    json_data = request.get_json()
    # 没有传送数据的情况
    if json_data is None:
        return message_json('data required')

    data = json.loads(json_data)
    item = BillItem(bill_info_id=data['bill_info_id'],
                    user_id=data['user_id']
                    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json())



# 跟新
@api.route('/bill_item/update')
def create_bill_item():
    json_data = request.get_json()
    # 没有传送数据的情况
    if json_data is None:
        return message_json('data required')

    data = json.loads(json_data)
    item = BillItem.query.get_or_404(json_data['item_id'])
    item.status=data['status']

    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json())

