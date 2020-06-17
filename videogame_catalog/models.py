from datetime import datetime

from videogame_catalog import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    publisher = db.Column(db.String(80), nullable=False)
    released_year = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.String(80), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Game %r for %r>' % self.name, self.platform
