from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))

    def __repr__(self):
        return f'User {self.username}'


class Pitch:
    '''
    Pitch class to define Movie Objects
    '''

    def __init__(self, id, title, post, poster, vote_average, vote_count):
        self.id = id
        self.title = title
        self.post = post


class Comment:
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pitch_id = db.Column(db.Integer, db.ForeignKey(
        'pitches.id'), nullable=False)

    # def save_comment(self):


    # @classmethod
    # def get_comments(cls, id):

    # for comment in cls.all_comments:
    #     if comment.pitch_id == id:


    # def __repr__(self):