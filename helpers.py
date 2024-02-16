#Creates extra function to check tokens for rightful action for our api (api interacts with the content that comes back within your app)
from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal
from models import User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]  # Bookmark for Insomnia
        if not token:
            return jsonify({'message': 'Token is missing.'}), 401

        current_user_token = User.query.filter_by(token = token).first()

        if not current_user_token:
            return jsonify({'message': 'Token is invalid'})
        
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)
