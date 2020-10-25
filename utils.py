from flask import jsonify


class Utils:
    def make_error(self, status_code, message, action):
        response = jsonify({
            'status': status_code,
            'message': message,
            'action': action
        })
        return response
