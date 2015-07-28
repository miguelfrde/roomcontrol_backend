# Room Control Backend

![TravisCI](https://travis-ci.org/miguelfrde/roomcontrol_backend.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/miguelfrde/roomcontrol_backend/badge.svg?branch=master&service=github)](https://coveralls.io/github/miguelfrde/roomcontrol_backend?branch=master)

**WARNING: Under development... WIP!**

Application built with Flask that interconnects the Raspberry Pi with the
[mobile application](https://github.com/miguelfrde/roomcontrol) to
control a room's lights, music, alarm and more.

## Requirements

- A Spotify app key is needed and it can be obtained [here](https://developer.spotify.com/technologies/libspotify/#application-keys).
Remember to choose binary, not C-Code.

- `libspotify`

## Setup for development

```
$ python setup.py develop
```

## Testing

```
$ flake8 .
$ py.test
```
