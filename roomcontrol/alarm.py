from flask import Blueprint

alarm_service = Blueprint('alarm', __name__)

@alarm_service.route('/')
def alarm():
    pass
