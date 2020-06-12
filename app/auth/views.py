
from flask import request, json, jsonify, logging, current_app
from . import auth
from .. import db
from ..models import User


@auth.route('/register', methods=['POST'])
def register():
    logger = logging.create_logger(current_app)
    # logger.info(f'$headers:\n{request.headers}')
    # logger.info('-------')
    # logger.info(f'$data:\n{request.data}')
    # json_data = request.get_json()
    # logger.info(f'json:\n${request.json} \n type: ${type(request.json)}')
    # # 没有传送数据的情况
    # if json_data is None:
    #     return jsonify({'message':'data required'})

    if request.data is None:
        return jsonify({'message':'data required'})
    data = json.loads(request.data)
    logger = logging.create_logger(current_app)
    # logger.info('name:'+data['name'])
    # logger.info('password:'+data['password'])
    if data['name'] is not None and data['password'] is not None:
        u= User(name=data['name'], password=data['password'])
        db.session.add(u)
        db.session.commit()
        return jsonify(u.to_json())
    else:
        return jsonify({'message': 'correct data required'})



@auth.route('/login', methods=['POST'])
def view_login():
    #logger = logging.create_logger(current_app)
    #logger.info(f'$data:\n{request.data}')
    # json_data = request.get_json()
    # # 没有传送数据的情况
    # if json_data is None:
    #     return jsonify({'message':'data required'})
    if request.data is None:
        return jsonify({'message': 'data required'})
    data = json.loads(request.data)

    if data['name'] is not None and data['password'] is not None:
        u = User.query.filter_by(name=data['name']).first()
        if u.verify_password(password=data['password'] ):
            return jsonify({
                "data": u.to_json(),
                "message": 'success',
                "status": 0
            })
        else:
            return jsonify({
                "data": {},
                "message": 'password or account incorrect',
                "status": -1
            })
    else:
        return jsonify({'message': 'correct data required'})
