from flask import Blueprint, request

alarm_service = Blueprint('alarm', __name__)


@alarm_service.route('', methods=['GET', 'POST'])
def alarm():
    if request.method == 'GET':
        return get_alarm_settings()
    else:
        return update_alarm_settings()


def update_alarm_settings():
    pass

def get_alarm_settings():
    pass
