from flask import Blueprint, request


light_service = Blueprint('light', __name__)


@light_service.route('', methods=['GET', 'POST'])
def light():
    if request.method == 'GET':
        return get_light_settings()
    else:
        return update_light_settings()


def get_light_settings():
    pass


def update_light_settings():
    pass
