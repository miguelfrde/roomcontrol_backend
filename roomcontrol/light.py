from flask import Blueprint

light_service = Blueprint('light', __name__)

@light_service.route('/')
def light():
    pass
