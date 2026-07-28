from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relasi ke Anime
    anime_list = db.relationship(
        "Anime",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"

class Anime(db.Model):
    __tablename__ = "anime"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    genre = db.Column(
        db.String(100),
        nullable=False
    )

    studio = db.Column(
        db.String(100),
        nullable=False
    )

    episodes = db.Column(
        db.Integer,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False
    )

    score = db.Column(
        db.Float,
        nullable=False
    )

    release_year = db.Column(
        db.Integer,
        nullable=False
    )

    cover_url = db.Column(
        db.String(500),
        nullable=True
    )

    synopsis = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Foreign Key
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Anime {self.title}>"