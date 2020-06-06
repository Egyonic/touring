"""
一些自己用的辅助函数
"""
import os
import uuid

from flask import jsonify

# 简单的带message的json
def message_json(msg):
    return jsonify({'message': msg
                    })

# 生产新的随机文件名的函数
def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename
