import logging

import click

from flask import Flask

from roomcontrol.services.alarm import alarm_service
from roomcontrol.services.light import light_service
from roomcontrol.services.main import main_service
from roomcontrol.services.music import music_service


@click.group(name='Room Control')
@click.option('--debug', default=False, is_flag=True,
              help='Show debugging logs')
@click.pass_context
def cli(ctx, debug):
    logging.basicConfig(level=logging.INFO)
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    ctx.obj['debug'] = debug


@cli.command(short_help='Start the server')
@click.pass_context
def serve(ctx):
    app = Flask(__name__)
    app.config['DEBUG'] = ctx.obj['debug']
    app.register_blueprint(main_service)
    app.register_blueprint(music_service, url_prefix='/music')
    app.register_blueprint(light_service, url_prefix='/light')
    app.register_blueprint(alarm_service, url_prefix='/alarm')
    app.run()


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
