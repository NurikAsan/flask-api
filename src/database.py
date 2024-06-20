import datetime
import string
import random
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    bookmarks = db.relationship('Bookmarks', backref='user')

    def __repr__(self):
        return f'<User {self.username}>'


class Bookmarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(100), nullable=False)
    short_url = db.Column(db.String(3), nullable=False)
    visitors = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    def generate_short_characters(self):
        characters = string.ascii_letters + string.digits
        picked_characters = ''.join(random.choices(characters, k=3))

        link = self.query.filter_by(short_url=picked_characters).first()

        if link:
            self.generate_short_characters()
        else:
            return picked_characters

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.short_url = self.generate_short_characters()

    def __repr__(self):
        return f'<Bookmarks {self.url}>'
