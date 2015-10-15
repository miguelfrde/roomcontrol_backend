# Room Control Backend

[![TravisCI](https://travis-ci.org/miguelfrde/roomcontrol_backend.svg?branch=master)](https://travis-ci.org/miguelfrde/roomcontrol_backend)
[![Coverage Status](https://coveralls.io/repos/miguelfrde/roomcontrol_backend/badge.svg?branch=master&service=github)](https://coveralls.io/github/miguelfrde/roomcontrol_backend?branch=master)

**WARNING: Under development... WIP!**

Application built with nameko that interconnects the Raspberry Pi with the
[mobile application](https://github.com/miguelfrde/roomcontrol) to
control a room's lights, music, alarm and more.

## Requirements

- A Spotify app key is needed and it can be obtained [here](https://developer.spotify.com/technologies/libspotify/#application-keys).
Remember to choose binary, not C-Code.

- `libspotify` (I suggest to follow [this](https://pyspotify.mopidy.com/en/latest/installation/))
- `RabbitMQ`

## Setup for development

```
$ pip install -e '.[dev]'
$ pip install pyaudio --allow-unverified=pyaudio --allow-external=PyAudio
$ pip install tox
```

## Testing

```
$ tox
```

## Routes

```
POST /login
GET /settings
POST /settings

GET /light
POST /light

GET /alarm
POST /alarm

GET /music/volume
POST /music/volume/<int:level>

GET /music/status
POST /music/pause
POST /music/play
POST /music/next
POST /music/previous

GET /music/trcks/current
GET /music/playlists/current
GET /music/playlists
GET /music/playlists/<int:id>
POST /music/playlists/<int:id>
```

## storage.cfg format

This data corresponds directly to the data saved in the
[mobile device](https://github.com/miguelfrde/roomcontrol#data-saved-to-the-device-local-storage).

```
[settings]
serverip=ip
notify=boolean
sendpic=boolean

[light]
intensity=int
status=boolean
color=hexadecimal

[alarm]
hour=int (epochs)
sound=int (id)
light=int (id)
active=boolean

[music]
playlist=int (id)
track=int (id)
volume=int
```
