import time

from nameko.events import event_handler
from nameko.timer import timer


class AlarmService:
    name = 'alarm_service'

    def __init__(self):
        self.hours = 0
        self.minutes = 0
        self.is_on = False
        self.light_program = None
        self.sound = None

    @event_handler("http_service", "alarm_settings_updated")
    def update_alarm(self, new_settings):
        t = time.localtime(new_settings['hour'])
        self.hours = t.tm_hour
        self.minutes = t.tm_min
        self.is_on = new_settings['active']
        if type(self.is_on) == str:
            self.is_on = self.is_on.lower() in ('true', 'on')
        self.light_program = new_settings['light']
        self.sound = new_settings['sound']

    @timer(interval=60)
    def fire_alarm(self):
        if not self.is_on:
            return
        now = time.localtime()
        if now.tm_hour == self.hours and now.tm_min == self.minutes:
            print("Fire alarm!")
