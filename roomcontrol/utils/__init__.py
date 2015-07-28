from functools import wraps

from flask import current_app, redirect, request


def ssl_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_app.config.get("SSL") and not request.is_secure:
            return redirect(request.url.replace("http://", "https://"))
        return fn(*args, **kwargs)
    return decorated_view
