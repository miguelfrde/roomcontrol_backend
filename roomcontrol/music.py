from flask import Blueprint

music_service = Blueprint('music', __name__)

@music_service.route('/')
def music():
    pass
