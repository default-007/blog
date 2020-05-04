from flask import render_template,request,redirect,url_for
from . import main
from ..models import Comment
from .forms import CommentForm

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Pitch . Space'
    pitches = Pitch.query.all()
    lyric = Pitch.query.filter_by(category = 'Lyric').all()
    sales = Pitch.query.filter_by(category = 'Sales').all()
    product = Pitch.query.filter_by(category = 'Product').all()

    return render_template('main.index.html',title = title,lyric = lyric, sales = sales, product = product)


@main.route('/user/<name>')
def profile(name):

    '''
    View profile page function that returns the profile details page and its data
    '''
    title = 'My Profile'
    user = User.query.filter_by(username = name).first()
    user_id = current_user._get_current_object().id

    return render_template('main.profile.html',title = title ,id = user_id)


@main.route('/comment/<int:pitch_id>', methods = ['POST','GET'])
def comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,pitch_id = pitch_id)
        new_comment.save_c()
        return redirect(url_for('.comment', pitch_id = pitch_id))
    return render_template('main.new_comment.html', comment_form =comment_form, pitch = pitch,all_comments=all_comments) 
