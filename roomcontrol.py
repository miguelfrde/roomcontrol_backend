from flask import Flask
from roomcontrol.music import music_service
from roomcontrol.light import light_service
from roomcontrol.alarm import alarm_service

app = Flask(__name__)
app.register_blueprint(music_service, url_prefix='/music')
app.register_blueprint(light_service, url_prefix='/light')
app.register_blueprint(alarm_service, url_prefix='/alarm')

@app.route('/login', methods=['POST'])
def login():
    pass

@app.route('/settings', methods=['GET', 'POST'])
def update_settings():
    pass

if __name__ == "__main__":
    app.run()
