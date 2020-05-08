from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import text
import jwt
import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255), unique=True, index=True)
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))

    pitches = db.relationship('Pitch',backref='user',lazy='dynamic')
    comments = db.relationship('Comment',backref='user',lazy='dynamic')
    upvotes = db.relationship('UpVote',backref='user',lazy='dynamic')
    downvotes = db.relationship('DownVote',backref='user',lazy='dynamic')
    
    
    
    @property
    def password(self):
        raise AttributeError("You can not read password attribute")
    
    @password.setter
    def password(self,password):
        self.hash_pass = generate_password_hash(password)
        
    def set_password(self, password):
        self.hash_pass = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.hash_pass, password)
    
    
    def __repr__(self):
        return f'User {self.username}'
    
    
class Pitch(db.Model):
    __tablename__ = 'pitches'
    
    id = db.Column(db.Integer, primary_key = True)
    pitch_content = db.Column(db.String())
    pitch_category = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def save_pitch(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def get_pitch(cls,id):
        pitches = Pitch.query.filter_by(id=id).all()
        return pitches
    
    @classmethod
    def get_all_pitches(cls):
        pitches = Pitch.query.order_by(text('-id')).all()
        return pitches
    
    @classmethod
    def get_category(cls, cat):
        category = Pitch.query.filter_by(pitch_category = cat).order_by(text('-id')).all()
        
        return category        
    

        
    
class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer,primary_key=True)
    comment_content = db.Column(db.String())
    pitch_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id')) 
    
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
        
    
    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(pitch_id=id).all()
        return comments
    
    
class UpVote(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitching_id = db.Column(db.Integer)
    
    def save_vote(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def get_votes(cls,id):
        upvote = UpVote.query.filter_by(pitching_id=id).all()
        return upvote   
    
       
    def __repr__(self):
        return f'{self.id_user}:{self.pitching_id}'
    
class DownVote(db.Model):
    __tablename__ = 'downvotes'
    
    id = db.Column(db.Integer, primary_key=True)
    
    id_user = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitching_id = db.Column(db.Integer)
    
    def save_vote(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_downvotes(cls,id):
        downvote = DownVote.query.filter_by(pitching_id=id).all()
        return downvote
    
        
    
    
    def __repr__(self):
        return f'{self.id_user}:{self.pitching_id}'