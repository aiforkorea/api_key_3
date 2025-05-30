from functools import wraps
from flask import request, current_app, abort
def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        # 보통 header에서 'x-api-key'로 받음
        key = request.headers.get('x-api-key') or request.args.get('api_key') or request.form.get('api_key')
        allowed_keys = current_app.config['API_KEY']
        if key and key in allowed_keys:
            return view_function(*args, **kwargs)
        else:
            abort(401, description="API Key is missing or invalid.")
    return decorated_function
