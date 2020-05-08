from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Comment, Pitch, User,UpVote,DownVote
from .forms import CommentForm, UpdateProfile, PitchForm
from .. import db, photos
from flask_login import login_required, current_user
import markdown2



# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Blog|Pitch'
   
    return render_template('index.html',title = title)


@main.route('/user/<uname>&<id_user>')
def profile(uname, id_user):

    '''
    View profile page function that returns the profile details page and its data
    '''
    title = 'My Profile'
    user = User.query.filter_by(username=uname).first()
    
    get_pitches = Pitch.query.filter_by(user_id = id_user).all()
    get_comments = Comment.query.filter_by(user_id = id_user).all()
    get_upvotes = UpVote.query.filter_by(id_user = id_user).all()
    get_downvotes = DownVote.query.filter_by(id_user=id_user).all()
    
    if user is None:
        abort(404)

    return render_template('profile/profile.html', user = user, title=title, pitches_no = get_pitches, comments_no = get_comments, likes_no = get_upvotes, dislikes_no = get_downvotes)

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

        return redirect(url_for('.profile',uname=user.username,id_user=user.id))

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
    return redirect(url_for('main.profile', uname=uname,id_user=current_user.id))
    

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


@main.route('/home/like/<int:id>', methods = ['GET','POST'])
@login_required
def like(id):
    get_pitches = UpVote.get_votes(id)
    valid_string = f'{current_user.id}:{id}'

    for get_pitch in get_pitches:
        to_str = f'{get_pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.pitch',id=id))
        else:
            continue

    like_pitch = UpVote(user = current_user, pitching_id=id)
    like_pitch.save_vote()

    return redirect(url_for('main.pitch',id=id))

@main.route('/home/dislike/<int:id>', methods = ['GET','POST'])
@login_required
def dislike(id):
    get_pitches = DownVote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'

    for get_pitch in get_pitches:
        to_str = f'{get_pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.pitch',id=id))
        else:
            continue

    dislike_pitch = DownVote(user = current_user, pitching_id=id)
    dislike_pitch.save_vote()

    return redirect(url_for('main.pitch',id=id))
