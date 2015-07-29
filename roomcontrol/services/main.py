from flask import Blueprint, request, jsonify

from roomcontrol.utils import ssl_required
import roomcontrol.utils.localstorage as ls

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
    return jsonify(ls.get_all('settings'))


def update_settings():
    settings = ls.get_all('settings')
    new_settings = request.get_json()
    for setting, value in new_settings.items():
        if setting in settings:
            print(setting)
            settings[setting] = str(value)
    ls.set_all('settings', settings)
    return 'settings updated'
