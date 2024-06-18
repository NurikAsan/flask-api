from flask import Blueprint


auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth.post('/register')
def register():
    return 'register'


@auth.get('/login')
def login():
    return {'login': 'Enter'}
