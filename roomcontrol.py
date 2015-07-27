from flask import Flask
from roomcontrol.main import main_service
from roomcontrol.music import music_service
from roomcontrol.light import light_service
from roomcontrol.alarm import alarm_service

app = Flask(__name__)
app.config['DEBUG'] = True

app.register_blueprint(main_service)
app.register_blueprint(music_service, url_prefix='/music')
app.register_blueprint(light_service, url_prefix='/light')
app.register_blueprint(alarm_service, url_prefix='/alarm')

if __name__ == "__main__":
    app.run()
