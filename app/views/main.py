# app/views/main.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from ..models.feedback import Feedback
from ..forms.feedback import ContactForm
from ..extensions import db
from ..models.interaction import Comment
from ..models.university import University, Course
from ..models.user import User
from sqlalchemy import or_

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/search')
def search_results():
    query_text = request.args.get('q', '')
    try:
        universities_query = University.query.filter(
            University.university_name.ilike(f"%{query_text}%")
        )
        universities = universities_query.all()

        courses_query = Course.query.filter(
            or_(
                Course.course_name.ilike(f"%{query_text}%"),
                Course.abbrv.ilike(f"%{query_text}%")
            )
        )
        courses = courses_query.all()

        return render_template(
            'search_results.html',
            query=query_text,
            universities=universities,
            courses=courses
        )
    except Exception as e:
        return render_template(
            'search_results.html',
            query=query_text,
            universities=[],
            courses=[],
            error="An error occurred while processing your search. Please try again."
        )

@bp.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('main.home'))
    return render_template('profile.html', user=user)

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        feedback = Feedback(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        try:
            db.session.add(feedback)
            db.session.commit()
            flash('Thank you for your feedback!', 'success')
        except:
            db.session.rollback()
            flash('An error occurred while saving your feedback. Please try again.', 'danger')

        return redirect(url_for('main.contact'))

    comments = Comment.query.order_by(Comment.date_posted.desc()).all()
    return render_template('contact.html', form=form, comments=comments)