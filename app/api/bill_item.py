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


# 暂时用不到这个方法
# item创建都是在BillInfo创建时一起创建的
# 创建
@api.route('/bill_item/new', methods=['POST'])
def create_bill_item():
    # json_data = request.get_json()
    # # 没有传送数据的情况
    # if json_data is None:
    #     return message_json('data required')
    #
    # data = json.loads(json_data)
    if request.data is None:
        return jsonify({'message': 'data required'})
    data = json.loads(request.data)

    item = BillItem(bill_info_id=data['bill_info_id'],
                    user_id=data['user_id']
                    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json())



# 跟新
@api.route('/bill_item/<int:iid>/update', methods=['POST'])
def update_bill_item(iid):
    item = BillItem.query.get_or_404(iid)
    # json_data = request.get_json()
    # # 没有传送数据的情况
    # if json_data is None:
    #     return message_json('data required')
    # data = json.loads(json_data)
    if request.data is None:
        return jsonify({'message': 'data required'})
    data = json.loads(request.data)

    item.status=data['status']

    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json())

