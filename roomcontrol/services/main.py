from flask import Blueprint, request

from roomcontrol.utils import ssl_required

main_service = Blueprint('main', __name__)


@main_service.route('/login', methods=['POST'])
@ssl_required
def login():
    pass


@main_service.route('/settings', methods=['GET', 'POST'])
def settings():
    print('settings called')
    if request.method == 'GET':
        return get_settings()
    else:
        return update_settings()


def get_settings():
    return 'settings'


def update_settings():
    return 'update settings'
