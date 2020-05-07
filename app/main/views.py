from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Comment, Pitch, User, Upvote, Downvote
from .forms import CommentForm, UpdateProfile, PitchForm
from .. import db, photos
from flask_login import login_required, current_user




# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Blog|Pitch'
   
    return render_template('index.html',title = title)


@main.route('/user/<uname>')
def profile(uname):

    '''
    View profile page function that returns the profile details page and its data
    '''
    title = 'My Profile'
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)
    

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))
    


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

@main.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    pitch_form = PitchForm()
    
    if pitch_form.validate_on_submit():
        pitch = pitch_form.pitch.data
        cat = pitch_form.my_category.data

        new_pitch = Pitch(pitch_content=pitch, pitch_category = cat, user = current_user)
        new_pitch.save_pitch()

        return redirect(url_for('main.home'))

    all_pitches = Pitch.get_all_pitches()

    title = 'Home | Blog|Pitch'    
    return render_template('home.html', title=title, pitch_form=pitch_form, pitches=all_pitches)
    
@main.route('/pitch/<int:id>',methods = ['GET','POST'])
@login_required
def pitch(id):
    
    my_pitch = Pitch.query.get(id)
    comment_form = CommentForm()
    

    if id is None:
        abort(404)

    if comment_form.validate_on_submit():
        comment_data = comment_form.comment.data
        new_comment = Comment(comment_content = comment_data, pitch_id = id, user = current_user)
        new_comment.save_comment()

        return redirect(url_for('main.pitch',id=id))

    all_comments = Comment.get_comments(id)


    # up_likes = UpVote.get_votes(id)
    # down_likes = DownVote.get_downvotes(id)

    title = 'Comment | One Minute Pitch'
    return render_template('pitch.html',pitch = my_pitch, comment_form = comment_form, comments = all_comments, title = title)

@main.route('/category/<cat>')
def category(cat):
    my_category = Pitch.get_category(cat)

    title = f'{cat} category | Blog|Pitch'

    return render_template('category.html', title=title, category=my_category)


@main.route('/pitch/upvote/<int:pitch_id>/upvote', methods = ['GET', 'POST'])
@login_required
def upvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_upvotes = Upvote.query.filter_by(pitch_id= pitch_id)
    
    if Upvote.query.filter(Upvote.user_id==user.id,Upvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.index'))


    new_upvote = Upvote(pitch_id=pitch_id, user = current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('main.index'))



#    new_upvote = Upvote(user=current_user, pitch=pitch, vote_number=1)
#    new_vote.save_vote()
# return redirect(url_for('main.index'))


@main.route('/pitch/downvote/<int:pitch_id>/downvote', methods = ['GET', 'POST'])
@login_required
def downvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_downvotes = Downvote.query.filter_by(pitch_id= pitch_id)
    
    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.index'))


    new_downvote = Downvote(pitch_id=pitch_id, user = current_user)
    new_downvote.save_downvotes()
    return redirect(url_for('main.index'))