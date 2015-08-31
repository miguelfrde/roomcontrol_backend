import logging
import os.path
import threading
from functools import wraps

from nameko.events import event_handler
from nameko.rpc import rpc

import spotify

from roomcontrol.services.base_service import BaseService


class SpotifyService(BaseService):
    name = 'spotify_service'

    STOPPED = 'stop'
    PLAYING = 'play'
    PAUSED = 'paused'

    STATES = (STOPPED, PLAYING, PAUSED)

    _LOGIN_DATAFILE = os.path.expanduser('~/.roomcontrol/spotifysession')

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = spotify.Session()
        self.loop = spotify.EventLoop(self.session)
        self.audio = spotify.PortAudioSink(self.session)
        self.current_state = SpotifyService.STOPPED
        self.loop.start()

    @rpc
    def login(self, user_id=None, password=None):
        logged_in_event = threading.Event()
        self.session.on(
            spotify.SessionEvent.CONNECTION_STATE_UPDATED,
            lambda s:
                self.__login_connection_state_listener(s, logged_in_event))

        if os.path.isfile(SpotifyService._LOGIN_DATAFILE):
            with open(SpotifyService._LOGIN_DATAFILE, 'rt') as f:
                user_id, blob = f.read().split('|')
                self.logger.info('Trying to login using the blob file')
                self.session.login(user_id, blob=blob, remember_me=True)
        else:
            self.session.on(
                spotify.SessionEvent.CREDENTIALS_BLOB_UPDATED,
                self.__login_credentials_blob_updated)
            self.session.login(user_id, password, remember_me=True)

        logged_in_event.wait()

    def __login_connection_state_listener(self, session, logged_in_event):
        if session.connection.state is spotify.ConnectionState.LOGGED_IN:
            logged_in_event.set()

    def __login_credentials_blob_updated(self, session, blob):
        with open(SpotifyService._LOGIN_DATAFILE, 'wt') as f:
            f.write(session.user_name + '|' + blob.decode('utf-8'))
        self.logger.info('Spotify session blob saved')

    def login_required(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            connstate = self.session.connection.state
            if connstate is spotify.ConnectionState.LOGGED_OUT:
                self.login()
            return f(self, *args, **kwargs)
        return wrapper

    def move_to_state(state):
        def decorator(f):
            @wraps(f)
            def wrapper(self, *args, **kwargs):
                if self.current_state in SpotifyService.STATES:
                    self.current_state = state
                return f(self, *args, **kwargs)
            return wrapper
        return decorator

    @rpc
    @login_required
    def playlists(self):
        playlists = self.session.playlist_container
        playlists.load()
        for playlist in playlists:
            if type(playlist) is spotify.Playlist:
                playlist.load()
        return [str(p.link) for p in playlists]

    @rpc
    @login_required
    def playlist_info(self, playlisturi):
        playlist = spotify.Playlist(self.session, uri=playlisturi)
        if not playlist.is_loaded:
            playlist.load()
        return {
            'name': playlist.name,
            'tracks': self.playlist_tracks(playlisturi),
            'spotify_uri': playlisturi
        }

    @rpc
    @login_required
    def playlist_tracks(self, playlisturi):
        playlist = spotify.Playlist(self.session, uri=playlisturi)
        if not playlist.is_loaded:
            playlist.load()
        return [str(track.link) for track in playlist.tracks]

    @rpc
    @login_required
    def track_info(self, trackuri):
        track = spotify.Track(self.session, trackuri)
        if not track.is_loaded:
            track.load()
        cover = track.album.cover(spotify.ImageSize.LARGE)
        return {
            'name': track.name,
            'artist': track.album.artist.load().name,
            'album_cover': cover.load().data_uri,
            'spotify_uri': trackuri
        }

    @rpc
    @login_required
    def play_track(self, trackuri):
        track = spotify.Track(self.session, trackuri)
        track.load()
        self.session.player.load(track)
        self.play()

    @event_handler('http_service', 'spotify_pause')
    @login_required
    @move_to_state(PAUSED)
    def pause(self):
        self.session.player.pause()

    @event_handler('http_service', 'spotify_play')
    @login_required
    @move_to_state(PLAYING)
    def play(self):
        self.session.player.play()

    @event_handler('http_service', 'spotify_stop')
    @login_required
    @move_to_state(STOPPED)
    def stop(self):
        self.session.player.pause()
        self.session.player.unload()

    @rpc
    def playing_status(self):
        return self.current_state
