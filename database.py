import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import pymysql

# Install PyMySQL as MySQLdb
pymysql.install_as_MySQLdb()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Thread(db.Model):
    """Forum thread model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    author_uid = db.Column(db.String(100), nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    reply_count = db.Column(db.Integer, default=0)
    
    # Relationship to replies
    replies = db.relationship('Reply', backref='thread', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Thread {self.title}>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'author_uid': self.author_uid,
            'author_name': self.author_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'reply_count': self.reply_count
        }


class Reply(db.Model):
    """Forum reply model"""
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_uid = db.Column(db.String(100), nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    


    def __repr__(self):
        return f'<Reply {self.id}>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'thread_id': str(self.thread_id),
            'content': self.content,
            'author_uid': self.author_uid,
            'author_name': self.author_name,
            'created_at': self.created_at,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes
        }


class Vote(db.Model):
    """Vote model for threads and replies"""
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False)  # Thread or Reply ID
    item_type = db.Column(db.String(10), nullable=False)  # 'thread' or 'reply'
    vote_type = db.Column(db.String(10), nullable=False)  # 'upvote' or 'downvote'
    user_uid = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate votes
    __table_args__ = (db.UniqueConstraint('item_id', 'item_type', 'user_uid', name='unique_vote'),)

    def __repr__(self):
        return f'<Vote {self.vote_type} on {self.item_type} {self.item_id}>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'item_id': str(self.item_id),
            'item_type': self.item_type,
            'vote_type': self.vote_type,
            'user_uid': self.user_uid,
            'created_at': self.created_at
        }