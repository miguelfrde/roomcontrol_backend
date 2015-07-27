import logging

import click
from flask import Flask

from roomcontrol.main import main_service
from roomcontrol.music import music_service
from roomcontrol.light import light_service
from roomcontrol.alarm import alarm_service

@click.command()
@click.option('--debug', default=False, is_flag=True)
def roomcontrol(debug):
    logging.basicConfig(level=logging.INFO)
    app = Flask(__name__)
    
    if debug:
        app.config['DEBUG'] = True
        logging.basicConfig(level=logging.DEBUG)

    app.register_blueprint(main_service)
    app.register_blueprint(music_service, url_prefix='/music')
    app.register_blueprint(light_service, url_prefix='/light')
    app.register_blueprint(alarm_service, url_prefix='/alarm')

    app.run()

if __name__ == "__main__":
    roomcontrol()
