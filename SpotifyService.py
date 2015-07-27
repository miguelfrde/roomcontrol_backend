import threading
import os.path
import logging
from functools import wraps

import spotify


class SpotifyService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = spotify.Session()
        self.loop = spotify.EventLoop(self.session)
        self.audio = spotify.PortAudioSink(self.session)
        self.loop.start()

    def login(self, user_id=None, password=None):
        logged_in_event = threading.Event()
        self.session.on(
            spotify.SessionEvent.CONNECTION_STATE_UPDATED,
            lambda s:
                self.__login_connection_state_listener(s, logged_in_event))

        if os.path.isfile('blobs/currentsession'):
            with open('blobs/currentsession', 'rt') as f:
                user_id, blob = f.read().split('|')
                self.logger.info('Trying to login using the blob file')
                self.session.login(user_id, blob=blob, remember_me=True)
        else:
            self.session.on(
                spotify.SessionEvent.CREDENTIALS_BLOB_UPDATED,
                lambda s, b: self.__login_credentials_blob_updated(s, b))
            self.session.login(user_id, password, remember_me=True)

        logged_in_event.wait()

    def __login_connection_state_listener(self, session, logged_in_event):
        if session.connection.state is spotify.ConnectionState.LOGGED_IN:
            logged_in_event.set()

    def __login_credentials_blob_updated(self, session, blob):
        with open('blobs/currentsession', 'wt') as f:
            f.write(session.user_name + '|' + blob.decode('utf-8'))
        self.logger.info('Blob saved')

    def login_required(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            connstate = self.session.connection.state
            if connstate is spotify.ConnectionState.LOGGED_OUT:
                self.login()
            return f(self, *args, **kwargs)
        return wrapper

    @login_required
    def playlists(self):
        playlists = self.session.playlist_container
        playlists.load()
        playlists = [p for p in playlists if isinstance(p, spotify.Playlist)]
        for playlist in playlists:
            playlist.load()
        return [str(p.link) for p in playlists]

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

    @login_required
    def playlist_tracks(self, playlisturi):
        playlist = spotify.Playlist(self.session, uri=playlisturi)
        if not playlist.is_loaded:
            playlist.load()
        return [str(track.link) for track in playlist.tracks]

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

    @login_required
    def play_track(self, trackuri):
        track = spotify.Track(self.session, trackuri)
        track.load()
        self.session.player.load(track)
        self.play()

    @login_required
    def pause(self):
        self.session.player.pause()

    @login_required
    def play(self):
        self.session.player.play()

    @login_required
    def stop(self):
        self.session.player.pause()
        self.session.player.unload()
