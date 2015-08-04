import eventlet
eventlet.monkey_patch()

import logging

import click

from nameko.runners import ServiceRunner

from roomcontrol.services.alarm_service import AlarmService
from roomcontrol.services.http_entrypoint import HttpEntrypointService
from roomcontrol.services.localstorage import LocalStorageService
from roomcontrol.services.spotify_service import SpotifyService


@click.group(name='Room Control')
@click.option('--debug', default=False, is_flag=True,
              help='Show debugging logs')
@click.pass_context
def cli(ctx, debug):
    logging.basicConfig(level=logging.INFO)
    if debug:
        logging.info('DEBUG mode: ON')
        logging.basicConfig(level=logging.DEBUG)


@cli.command(short_help='Start all services')
def run():
    config = {'AMQP_URI': 'amqp://localhost'}
    runner = ServiceRunner(config)
    runner.add_service(AlarmService)
    runner.add_service(HttpEntrypointService)
    runner.add_service(LocalStorageService)
    runner.add_service(SpotifyService)
    runner.start()

    runnlet = eventlet.spawn(runner.wait)

    try:
        runnlet.wait()
    except KeyboardInterrupt:
        try:
            runner.stop()
        except KeyboardInterrupt:
            runner.kill()


def main():
    cli()


if __name__ == "__main__":
    main()
