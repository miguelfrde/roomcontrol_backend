from nameko.events import event_handler
from nameko.rpc import rpc

from roomcontrol.services.base_service import BaseService


class VolumeService(BaseService):
    name = 'volume_service'

    @rpc
    def get(self):
        pass

    @event_handler('http_service', 'volume_update')
    def set(self, level):
        pass
