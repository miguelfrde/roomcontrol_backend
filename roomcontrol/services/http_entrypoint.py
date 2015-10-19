import json

from nameko.events import EventDispatcher
from nameko.rpc import RpcProxy
from nameko.web.handlers import http

from roomcontrol.services.base_service import BaseService


class HttpEntrypointService(BaseService):
    name = 'http_service'

    dispatch = EventDispatcher()
    spotify_rpc = RpcProxy('spotify_rpc')

    @http('POST', '/login')
    def login(self, request):
        pass

    @http('GET', '/settings')
    def get_settings(self, request):
        return json.dumps(self.storage_rpc.get_all('settings'))

    @http('POST', '/settings')
    def update_settings(self, request):
        settings = json.loads(request.get_data().decode('utf-8'))
        self.save('settings', settings)
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
    # Volume entrypoints

    @http('GET', '/music/volume')
    def get_volume(self, request):
        return self.volume.get()

    @http('POST', '/music/volume/<int:level>')
    def update_volume(self, request, level):
        self.dispatch('update_volume', level)
        return 'Update volume requested'

    ##
    # Music entrypoints

    @http('GET', '/music/status')
    def music_status(self, request):
        return self.spotify_rpc.playing_status()

    @http('POST', '/music/play/playlists/<int:playlist_id>')
    def play_playlist(self, request, playlist_id):
        self.dispatch('spotify_play_playlist', playlist_id)
        return 'Spotify play playlist requested'

    @http('POST', '/music/play')
    def play(self, request):
        self.dispatch('spotify_play')
        return 'Spotify play requested'

    @http('POST', '/music/pause')
    def pause(self, request):
        self.dispatch('spotify_pause')
        return 'Spotify pause requested'

    @http('POST', '/music/next')
    def next_song(self, request):
        self.dispatch('spotify_next')
        return 'Spotify next song requested'

    @http('POST', '/music/previous')
    def previous_song(self, request):
        self.dispatch('spotify_previous')
        return 'Spotify previouse song requested'

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
