from flask import Blueprint, request


music_service = Blueprint('music', __name__)


@music_service.route('/volume', methods=['GET', 'POST'])
def volume():
    if request.method == 'GET':
        return get_volume()
    else:
        return update_volume()


@music_service.route('/status', methods=['GET'])
def music_status():
    pass


@music_service.route('/play', methods=['POST'])
def play():
    pass


@music_service.route('/play/playlists/<int:id>', methods=['POST'])
def play_playlist():
    pass


@music_service.route('/pause', methods=['POST'])
def pause():
    pass


@music_service.route('/next', methods=['POST'])
def next_song():
    pass


@music_service.route('/previous', methods=['POST'])
def previous_song():
    pass


@music_service.route('/tracks/current', methods=['GET'])
def current_track():
    pass


@music_service.route('/playlists/current', methods=['GET'])
def current_playlist():
    pass


@music_service.route('/playlists', methods=['GET'])
def playlists():
    pass


@music_service.route('/playlists/<int:id>', methods=['GET'])
def get_playlist():
    pass


def get_volume():
    pass


def update_volume():
    pass
