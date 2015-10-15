import time

from nameko.events import event_handler
from nameko.timer import timer

from roomcontrol.services.base_service import BaseService


class AlarmService(BaseService):
    name = 'alarm_service'

    def __init__(self):
        super().__init__()
        defaults = self.storage_rpc.get_all('alarm')
        t = defaults['hour']
        self.hours = t.tm_hour
        self.minutes = t.tm_min
        self.is_on = self.__on_str(defaults['active'])
        self.light_program = defaults['light']
        self.sound = defaults['sound']

    def __on_str(self, value):
        if type(value) == str:
            self.value = self.value.lower() in ('true', 'on')
        if self.value is None:
            return False
        return value

    @event_handler('http_service', 'alarm_settings_updated')
    def update_alarm(self, new_settings):
        t = time.localtime(new_settings['hour'])
        self.hours = t.tm_hour
        self.minutes = t.tm_min
        self.is_on = self.__on_str(new_settings['active'])
        self.light_program = new_settings['light']
        self.sound = new_settings['sound']
        self._save('alarm', new_settings)

    @timer(interval=60)
    def fire_alarm(self):
        if not self.is_on:
            return
        now = time.localtime()
        if now.tm_hour == self.hours and now.tm_min == self.minutes:
            print('Fire alarm!')
