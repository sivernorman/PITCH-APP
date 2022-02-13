from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Pitch,Comment,Upvote,Downvote
from .. import db,photos
from .forms import PitchForm,CommentForm,updateProfile
from flask_login import login_required,current_user
import datetime

@main.route('/')
def index():
 
    title = 'Home - Welcome to  Pitch App'
    pitches=Pitch.query.all()
    pickup = Pitch.query.filter_by(category='pickup').all()
    product = Pitch.query.filter_by(category='product').all()
    promotion = Pitch.query.filter_by(category='promotion').all()
    interview = Pitch.query.filter_by(category='interview').all()


    return render_template('index.html',pitch=pitches,title = title, interview = interview, product = product, promotion = promotion,pickup=pickup)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    pitches_count = Pitch.count_pitches(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,pitches = pitches_count,date = user_joined)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = updateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form = form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/new_pitch', methods = ['GET','POST'])
@login_required
         
def new_pitch():
    pitch_form = PitchForm()
    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        pitch = pitch_form.text.data
        category = pitch_form.category.data

        # Updated pitch instance
        new_pitch = Pitch(title=title,content=pitch,category=category,user=current_user)

        # Save pitch method
        new_pitch.save_pitch()


        return redirect(url_for('.index'))

    title = 'New pitch'
    return render_template('new_pitch.html',title = title,pitch_form=pitch_form )


@main.route('/pitch/<int:id>', methods = ['GET','POST'])
def pitch(id):
    pitch = Pitch.get_pitch(id)
    posted_date = pitch.posted.strftime('%b %d, %Y')

    if request.args.get("like"):
        pitch.likes = pitch.likes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    elif request.args.get("dislike"):
        pitch.dislikes = pitch.dislikes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comment(comment = comment,user = current_user,pitch_id = pitch)

        new_comment.save_comment()


    comments = Comment.get_comments(pitch)

    return render_template("pitch.html", pitch = pitch, comment_form = comment_form, comments = comments, date = posted_date)


@main.route('/comment/<id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    comment_form = CommentForm()
    pitch = Pitch.query.get(id)
    fetch_all_comments = Comment.query.filter_by(pitch_id=id).all()
    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        pitch_id = id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment=comment, user_id=user_id, pitch_id=pitch_id)
        new_comment.save_comment()
        return redirect(url_for('.comment', id=pitch_id))
    return render_template('comment.html', comment_form=comment_form, pitch=pitch, all_comments=fetch_all_comments)



@main.route('/user/<uname>/pitches')
def user_pitches(uname):
    user = User.query.filter_by(username=uname).first()
    pitches = Pitch.query.filter_by(user_id = user.id).all()
    pitches_count = Pitch.count_pitches(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    return render_template("profile/pitch.html", user=user,pitches=pitches,pitches_count=pitches_count,date = user_joined)



@main.route('/upvote/<id>', methods=['GET', 'POST'])
@login_required
def upVote(id):
    votes = Upvote.get_upvotes(id)
    output = f'{current_user.id}:{id}'
    for vote in votes:
        result = f'{vote}'
        if output == result:
            return redirect(url_for('main.index', id=id))
        else:
            continue
    new_upvote = Upvote(user=current_user, pitch_id=id)
    new_upvote.save()
    return redirect(url_for('main.index', id=id))


@main.route('/downvote/<id>', methods=['GET', 'POST'])
@login_required
def downVote(id):
    votes = Downvote.get_downvotes(id)
    output = f'{current_user.id}:{id}'
    for vote in votes:
        result = f'{vote}'
        if output == result:
            return redirect(url_for('main.index', id=id))
        else:
            continue
    new_downvote = Downvote(user=current_user, pitch_id=id)
    new_downvote.save()
    return redirect(url_for('main.index', id=id))


