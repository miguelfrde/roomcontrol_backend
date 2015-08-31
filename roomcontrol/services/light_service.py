from nameko.events import event_handler
from nameko.rpc import rpc

from roomcontrol.services.base_service import BaseService


class LightService(BaseService):
    name = 'light_service'

    @rpc
    def available_colors(self):
        pass

    @event_handler('http_service', 'light_turn_on')
    def turn_on(self):
        pass

    @event_handler('http_service', 'light_turn_off')
    def turn_off(self):
        pass

    @event_handler('http_service', 'light_set_color')
    def set_color(self, new_color):
        pass

    @event_handler('http_service', 'light_set_intensity')
    def set_intensity(self, level):
        pass
