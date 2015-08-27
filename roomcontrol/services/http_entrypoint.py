import json

from nameko.events import EventDispatcher
from nameko.web.handlers import http

from roomcontrol.services.base_service import BaseService


class HttpEntrypointService(BaseService):
    name = 'http_service'

    dispatch = EventDispatcher()

    @http('POST', '/login')
    def login(self, request):
        pass

    @http('GET', '/settings')
    def get_settings(self, request):
        return json.dumps(self.storage_rpc.get_all('settings'))

    @http('POST', '/settings')
    def update_settings(self, request):
        settings = json.loads(request.get_data().decode('utf-8'))
        self._save('settings', settings)
        return 'settings updated'

    ##
    # Alarm entrypoints

    @http('POST', '/alarm')
    def update_alarm_settings(self, request):
        alarm_settings = json.loads(request.get_data().decode('utf-8'))
        self.dispatch('alarm_settings_updated', alarm_settings)
        return 'alarm settings updated'

    @http('GET', '/alarm')
    def get_alarm_settings(self, request):
        return json.dumps(self.storage_rpc.get_all('alarm'))

    ##
    # Light entrypoints

    @http('POST', '/light')
    def update_light_settings(self, request):
        pass

    @http('GET', '/light')
    def get_light_settings(self, request):
        pass

    ##
    # Music entrypoints

    @http('GET', '/music/volume')
    def get_volume(self, request):
        pass

    @http('POST', '/music/volume')
    def update_volume(self, request):
        pass

    @http('GET', '/music/status')
    def music_status(self, request):
        pass

    @http('POST', '/music/play')
    def play(self, request):
        pass

    @http('POST', '/music/play/playlists/<int:playlist_id>')
    def play_playlist(self, request, playlist_id):
        pass

    @http('POST', '/music/pause')
    def pause(self, request):
        pass

    @http('POST', '/music/next')
    def next_song(self, request):
        pass

    @http('POST', '/music/previous')
    def previous_song(self, request):
        pass

    @http('GET', '/tracks/current')
    def current_track(self, request):
        pass

    @http('GET', '/playlists/current')
    def current_playlist(self, request):
        pass

    @http('GET', '/playlists')
    def playlists(self, request):
        pass

    @http('GET', '/playlists/<int:id>')
    def get_playlist(self, request):
        pass
