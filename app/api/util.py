"""
一些自己用的辅助函数
"""

from flask import jsonify

# 简单的带message的json
def message_json(msg):
    return jsonify({'message': msg
                    })
