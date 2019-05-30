from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from PIL import Image
import secrets
import os
import bs4
import requests
import re
from time import gmtime, strftime, sleep, time
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime, timedelta, time
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
import unicodedata
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail, Message
'''
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


scheduler = BackgroundScheduler()

scheduler.add_job(func=print_date_time, trigger="interval", seconds=3)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
'''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.db'
app.config['SECRET_KEY'] = 'f874123aa5dsf84af'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'projektjidelna@gmail.com'
app.config['MAIL_PASSWORD'] = 'ProjektJidelna123'
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    likeAuthor = db.relationship('User', backref='likeAuthor', lazy=True)



class PostLove(db.Model):
    __tablename__ = 'post_love'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    loveAuthor = db.relationship('User', backref='loveAuthor', lazy=True)


class PostConfused(db.Model):
    __tablename__ = 'post_confused'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    confusedAuthor = db.relationship('User', backref='confusedAuthor', lazy=True)


class PostAngry(db.Model):
    __tablename__ = 'post_angry'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    angryAuthor = db.relationship('User', backref='angryAuthor', lazy=True)


class PostSurprised(db.Model):
    __tablename__ = 'post_surprised'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    surprisedAuthor = db.relationship('User', backref='surprisedAuthor', lazy=True)


class PostSad(db.Model):
    __tablename__ = 'post_sad'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    sadAuthor = db.relationship('User', backref='sadAuthor', lazy=True)


class PostLaugh(db.Model):
    __tablename__ = 'post_laugh'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    laughAuthor = db.relationship('User', backref='laughAuthor', lazy=True)







class PostPriznaniLike(db.Model):
    __tablename__ = 'post_priznani_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    priznani_id = db.Column(db.Integer, db.ForeignKey('priznani.id'))
    likePriznaniAuthor = db.relationship('User', backref='likePriznaniAuthor', lazy=True)


class PostPriznaniLove(db.Model):
    __tablename__ = 'post_priznani_love'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    priznani_id = db.Column(db.Integer, db.ForeignKey('priznani.id'))
    lovePriznaniAuthor = db.relationship('User', backref='lovePriznaniAuthor', lazy=True)


class PostPriznaniConfused(db.Model):
    __tablename__ = 'post_priznani_confused'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    priznani_id = db.Column(db.Integer, db.ForeignKey('priznani.id'))
    confusedPriznaniAuthor = db.relationship('User', backref='confusedPriznaniAuthor', lazy=True)


class PostPriznaniAngry(db.Model):
    __tablename__ = 'post_priznani_angry'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    priznani_id = db.Column(db.Integer, db.ForeignKey('priznani.id'))
    angryPriznaniAuthor = db.relationship('User', backref='angryPriznaniAuthor', lazy=True)


class PostPriznaniSurprised(db.Model):
    __tablename__ = 'post_priznani_surprised'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    priznani_id = db.Column(db.Integer, db.ForeignKey('priznani.id'))
    surprisedPriznaniAuthor = db.relationship('User', backref='surprisedPriznaniAuthor', lazy=True)


class PostPriznaniSad(db.Model):
    __tablename__ = 'post_priznani_sad'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    priznani_id = db.Column(db.Integer, db.ForeignKey('priznani.id'))
    sadPriznaniAuthor = db.relationship('User', backref='sadPriznaniAuthor', lazy=True)


class PostPriznaniLaugh(db.Model):
    __tablename__ = 'post_priznani_laugh'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    priznani_id = db.Column(db.Integer, db.ForeignKey('priznani.id'))
    laughPriznaniAuthor = db.relationship('User', backref='laughPriznaniAuthor', lazy=True)







class PostHlaskaLike(db.Model):
    __tablename__ = 'post_hlaska_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hlaska_id = db.Column(db.Integer, db.ForeignKey('hlaska.id'))
    likeHlaskaAuthor = db.relationship('User', backref='likeHlaskaAuthor', lazy=True)


class PostHlaskaLove(db.Model):
    __tablename__ = 'post_hlaska_love'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hlaska_id = db.Column(db.Integer, db.ForeignKey('hlaska.id'))
    loveHlaskaAuthor = db.relationship('User', backref='loveHlaskaAuthor', lazy=True)


class PostHlaskaConfused(db.Model):
    __tablename__ = 'post_hlaska_confused'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hlaska_id = db.Column(db.Integer, db.ForeignKey('hlaska.id'))
    confusedHlaskaAuthor = db.relationship('User', backref='confusedHlaskaAuthor', lazy=True)


class PostHlaskaAngry(db.Model):
    __tablename__ = 'post_hlaska_angry'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hlaska_id = db.Column(db.Integer, db.ForeignKey('hlaska.id'))
    angryHlaskaAuthor = db.relationship('User', backref='angryHlaskaAuthor', lazy=True)


class PostHlaskaSurprised(db.Model):
    __tablename__ = 'post_hlaska_surprised'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hlaska_id = db.Column(db.Integer, db.ForeignKey('hlaska.id'))
    surprisedHlaskaAuthor = db.relationship('User', backref='surprisedHlaskaAuthor', lazy=True)


class PostHlaskaSad(db.Model):
    __tablename__ = 'post_hlaska_sad'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hlaska_id = db.Column(db.Integer, db.ForeignKey('hlaska.id'))
    sadHlaskaAuthor = db.relationship('User', backref='sadHlaskaAuthor', lazy=True)


class PostHlaskaLaugh(db.Model):
    __tablename__ = 'post_hlaska_laugh'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hlaska_id = db.Column(db.Integer, db.ForeignKey('hlaska.id'))
    laughHlaskaAuthor = db.relationship('User', backref='laughHlaskaAuthor', lazy=True)




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    icanteen = db.Column(db.String(20))
    icanteen_heslo = db.Column(db.String(20))
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    ratings = db.relationship('Rating', backref='author', lazy=True)
    hlasky = db.relationship('Hlaska', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    comments_priznani = db.relationship('CommentPriznani', backref='author', lazy=True)
    comments_hlaska = db.relationship('CommentHlaska', backref='author', lazy=True)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    liked = db.relationship('PostLike', foreign_keys='PostLike.user_id', backref='user', lazy='dynamic')
    loved = db.relationship('PostLove', foreign_keys='PostLove.user_id', backref='user', lazy='dynamic')
    confused = db.relationship('PostConfused', foreign_keys='PostConfused.user_id', backref='user', lazy='dynamic')
    angry = db.relationship('PostAngry', foreign_keys='PostAngry.user_id', backref='user', lazy='dynamic')
    surprised = db.relationship('PostSurprised', foreign_keys='PostSurprised.user_id', backref='user', lazy='dynamic')
    sad = db.relationship('PostSad', foreign_keys='PostSad.user_id', backref='user', lazy='dynamic')
    laugh = db.relationship('PostLaugh', foreign_keys='PostLaugh.user_id', backref='user', lazy='dynamic')
    liked_priznani = db.relationship('PostPriznaniLike', foreign_keys='PostPriznaniLike.user_id', backref='user', lazy='dynamic')
    loved_priznani = db.relationship('PostPriznaniLove', foreign_keys='PostPriznaniLove.user_id', backref='user', lazy='dynamic')
    confused_priznani = db.relationship('PostPriznaniConfused', foreign_keys='PostPriznaniConfused.user_id', backref='user', lazy='dynamic')
    angry_priznani = db.relationship('PostPriznaniAngry', foreign_keys='PostPriznaniAngry.user_id', backref='user', lazy='dynamic')
    surprised_priznani = db.relationship('PostPriznaniSurprised', foreign_keys='PostPriznaniSurprised.user_id', backref='user', lazy='dynamic')
    sad_priznani = db.relationship('PostPriznaniSad', foreign_keys='PostPriznaniSad.user_id', backref='user', lazy='dynamic')
    laugh_priznani = db.relationship('PostPriznaniLaugh', foreign_keys='PostPriznaniLaugh.user_id', backref='user', lazy='dynamic')
    likeHlaska = db.relationship('PostHlaskaLike', foreign_keys='PostHlaskaLike.user_id', backref='user', lazy='dynamic')
    loveHlaska = db.relationship('PostHlaskaLove', foreign_keys='PostHlaskaLove.user_id', backref='user', lazy='dynamic')
    confuseHlaska = db.relationship('PostHlaskaConfused', foreign_keys='PostHlaskaConfused.user_id', backref='user', lazy='dynamic')
    angrHlaska = db.relationship('PostHlaskaAngry', foreign_keys='PostHlaskaAngry.user_id', backref='user', lazy='dynamic')
    surpriseHlaska = db.relationship('PostHlaskaSurprised', foreign_keys='PostHlaskaSurprised.user_id', backref='user', lazy='dynamic')
    saHlaska = db.relationship('PostHlaskaSad', foreign_keys='PostHlaskaSad.user_id', backref='user', lazy='dynamic')
    laugHlaska = db.relationship('PostHlaskaLaugh', foreign_keys='PostHlaskaLaugh.user_id', backref='user', lazy='dynamic')
    obsidianUser = db.Column(db.Integer)
    diamondUser = db.Column(db.Integer)
    platinumUser = db.Column(db.Integer)
    goldUser = db.Column(db.Integer)
    silverUser = db.Column(db.Integer)
    bronzeUser = db.Column(db.Integer)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_secret_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(PostLike.user_id == self.id, PostLike.post_id == post.id).count() > 0

    def love_post(self, post):
        if not self.has_loved_post(post):
            love = PostLove(user_id=self.id, post_id=post.id)
            db.session.add(love)

    def unlove_post(self, post):
        if self.has_loved_post(post):
            PostLove.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_loved_post(self, post):
        return PostLove.query.filter(PostLove.user_id == self.id, PostLove.post_id == post.id).count() > 0

    def confuse_post(self, post):
        if not self.has_confused_post(post):
            confuse = PostConfused(user_id=self.id, post_id=post.id)
            db.session.add(confuse)

    def unconfuse_post(self, post):
        if self.has_confused_post(post):
            PostConfused.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_confused_post(self, post):
        return PostConfused.query.filter(PostConfused.user_id == self.id, PostConfused.post_id == post.id).count() > 0

    def angry_post(self, post):
        if not self.has_angry_post(post):
            angry = PostAngry(user_id=self.id, post_id=post.id)
            db.session.add(angry)

    def unangry_post(self, post):
        if self.has_angry_post(post):
            PostAngry.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_angry_post(self, post):
        return PostAngry.query.filter(PostAngry.user_id == self.id, PostAngry.post_id == post.id).count() > 0

    def surprise_post(self, post):
        if not self.has_surprise_post(post):
            surprise = PostSurprised(user_id=self.id, post_id=post.id)
            db.session.add(surprise)

    def unsurprise_post(self, post):
        if self.has_surprise_post(post):
            PostSurprised.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_surprise_post(self, post):
        return PostSurprised.query.filter(PostSurprised.user_id == self.id, PostSurprised.post_id == post.id).count() > 0

    def sad_post(self, post):
        if not self.has_sad_post(post):
            sad = PostSad(user_id=self.id, post_id=post.id)
            db.session.add(sad)

    def unsad_post(self, post):
        if self.has_sad_post(post):
            PostSad.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_sad_post(self, post):
        return PostSad.query.filter(PostSad.user_id == self.id, PostSad.post_id == post.id).count() > 0

    def laugh_post(self, post):
        if not self.has_laugh_post(post):
            laugh = PostLaugh(user_id=self.id, post_id=post.id)
            db.session.add(laugh)

    def unlaugh_post(self, post):
        if self.has_laugh_post(post):
            PostLaugh.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_laugh_post(self, post):
        return PostLaugh.query.filter(PostLaugh.user_id == self.id, PostLaugh.post_id == post.id).count() > 0




    def like_priznani_post(self, post):
        if not self.has_liked_priznani_post(post):
            like = PostPriznaniLike(user_id=self.id, priznani_id=post.id)
            db.session.add(like)

    def unlike_priznani_post(self, post):
        if self.has_liked_priznani_post(post):
            PostPriznaniLike.query.filter_by(
                user_id=self.id,
                priznani_id=post.id).delete()

    def has_liked_priznani_post(self, post):
        return PostPriznaniLike.query.filter(PostPriznaniLike.user_id == self.id, PostPriznaniLike.priznani_id == post.id).count() > 0

    def love_priznani_post(self, post):
        if not self.has_loved_priznani_post(post):
            love = PostPriznaniLove(user_id=self.id, priznani_id=post.id)
            db.session.add(love)

    def unlove_priznani_post(self, post):
        if self.has_loved_priznani_post(post):
            PostPriznaniLove.query.filter_by(
                user_id=self.id,
                priznani_id=post.id).delete()

    def has_loved_priznani_post(self, post):
        return PostPriznaniLove.query.filter(PostPriznaniLove.user_id == self.id, PostPriznaniLove.priznani_id == post.id).count() > 0

    def confuse_priznani_post(self, post):
        if not self.has_confused_priznani_post(post):
            confuse = PostPriznaniConfused(user_id=self.id, priznani_id=post.id)
            db.session.add(confuse)

    def unconfuse_priznani_post(self, post):
        if self.has_confused_priznani_post(post):
            PostPriznaniConfused.query.filter_by(
                user_id=self.id,
                priznani_id=post.id).delete()

    def has_confused_priznani_post(self, post):
        return PostPriznaniConfused.query.filter(PostPriznaniConfused.user_id == self.id, PostPriznaniConfused.priznani_id == post.id).count() > 0

    def angry_priznani_post(self, post):
        if not self.has_angry_priznani_post(post):
            angry = PostPriznaniAngry(user_id=self.id, priznani_id=post.id)
            db.session.add(angry)

    def unangry_priznani_post(self, post):
        if self.has_angry_priznani_post(post):
            PostPriznaniAngry.query.filter_by(
                user_id=self.id,
                priznani_id=post.id).delete()

    def has_angry_priznani_post(self, post):
        return PostPriznaniAngry.query.filter(PostPriznaniAngry.user_id == self.id, PostPriznaniAngry.priznani_id == post.id).count() > 0

    def surprise_priznani_post(self, post):
        if not self.has_surprise_priznani_post(post):
            surprise = PostPriznaniSurprised(user_id=self.id, priznani_id=post.id)
            db.session.add(surprise)

    def unsurprise_priznani_post(self, post):
        if self.has_surprise_priznani_post(post):
            PostPriznaniSurprised.query.filter_by(
                user_id=self.id,
                priznani_id=post.id).delete()

    def has_surprise_priznani_post(self, post):
        return PostPriznaniSurprised.query.filter(PostPriznaniSurprised.user_id == self.id, PostPriznaniSurprised.priznani_id == post.id).count() > 0

    def sad_priznani_post(self, post):
        if not self.has_sad_priznani_post(post):
            sad = PostPriznaniSad(user_id=self.id, priznani_id=post.id)
            db.session.add(sad)

    def unsad_priznani_post(self, post):
        if self.has_sad_priznani_post(post):
            PostPriznaniSad.query.filter_by(
                user_id=self.id,
                priznani_id=post.id).delete()

    def has_sad_priznani_post(self, post):
        return PostPriznaniSad.query.filter(PostPriznaniSad.user_id == self.id, PostPriznaniSad.priznani_id == post.id).count() > 0

    def laugh_priznani_post(self, post):
        if not self.has_laugh_priznani_post(post):
            laugh = PostPriznaniLaugh(user_id=self.id, priznani_id=post.id)
            db.session.add(laugh)

    def unlaugh_priznani_post(self, post):
        if self.has_laugh_priznani_post(post):
            PostPriznaniLaugh.query.filter_by(
                user_id=self.id,
                priznani_id=post.id).delete()

    def has_laugh_priznani_post(self, post):
        return PostPriznaniLaugh.query.filter(PostPriznaniLaugh.user_id == self.id, PostPriznaniLaugh.priznani_id == post.id).count() > 0



    def like_hlaska_post(self, post):
        if not self.has_liked_hlaska_post(post):
            like = PostHlaskaLike(user_id=self.id, hlaska_id=post.id)
            db.session.add(like)

    def unlike_hlaska_post(self, post):
        if self.has_liked_hlaska_post(post):
            PostHlaskaLike.query.filter_by(
                user_id=self.id,
                hlaska_id=post.id).delete()

    def has_liked_hlaska_post(self, post):
        return PostHlaskaLike.query.filter(PostHlaskaLike.user_id == self.id, PostHlaskaLike.hlaska_id == post.id).count() > 0

    def love_hlaska_post(self, post):
        if not self.has_loved_hlaska_post(post):
            love = PostHlaskaLove(user_id=self.id, hlaska_id=post.id)
            db.session.add(love)

    def unlove_hlaska_post(self, post):
        if self.has_loved_hlaska_post(post):
            PostHlaskaLove.query.filter_by(
                user_id=self.id,
                hlaska_id=post.id).delete()

    def has_loved_hlaska_post(self, post):
        return PostHlaskaLove.query.filter(PostHlaskaLove.user_id == self.id, PostHlaskaLove.hlaska_id == post.id).count() > 0

    def confuse_hlaska_post(self, post):
        if not self.has_confused_hlaska_post(post):
            confuse = PostHlaskaConfused(user_id=self.id, hlaska_id=post.id)
            db.session.add(confuse)

    def unconfuse_hlaska_post(self, post):
        if self.has_confused_hlaska_post(post):
            PostHlaskaConfused.query.filter_by(
                user_id=self.id,
                hlaska_id=post.id).delete()

    def has_confused_hlaska_post(self, post):
        return PostHlaskaConfused.query.filter(PostHlaskaConfused.user_id == self.id, PostHlaskaConfused.hlaska_id == post.id).count() > 0

    def angry_hlaska_post(self, post):
        if not self.has_angry_hlaska_post(post):
            angry = PostHlaskaAngry(user_id=self.id, hlaska_id=post.id)
            db.session.add(angry)

    def unangry_hlaska_post(self, post):
        if self.has_angry_hlaska_post(post):
            PostHlaskaAngry.query.filter_by(
                user_id=self.id,
                hlaska_id=post.id).delete()

    def has_angry_hlaska_post(self, post):
        return PostHlaskaAngry.query.filter(PostHlaskaAngry.user_id == self.id, PostHlaskaAngry.hlaska_id == post.id).count() > 0

    def surprise_hlaska_post(self, post):
        if not self.has_surprise_hlaska_post(post):
            surprise = PostHlaskaSurprised(user_id=self.id, hlaska_id=post.id)
            db.session.add(surprise)

    def unsurprise_hlaska_post(self, post):
        if self.has_surprise_hlaska_post(post):
            PostHlaskaSurprised.query.filter_by(
                user_id=self.id,
                hlaska_id=post.id).delete()

    def has_surprise_hlaska_post(self, post):
        return PostHlaskaSurprised.query.filter(PostHlaskaSurprised.user_id == self.id, PostHlaskaSurprised.hlaska_id == post.id).count() > 0

    def sad_hlaska_post(self, post):
        if not self.has_sad_hlaska_post(post):
            sad = PostHlaskaSad(user_id=self.id, hlaska_id=post.id)
            db.session.add(sad)

    def unsad_hlaska_post(self, post):
        if self.has_sad_hlaska_post(post):
            PostHlaskaSad.query.filter_by(
                user_id=self.id,
                hlaska_id=post.id).delete()

    def has_sad_hlaska_post(self, post):
        return PostHlaskaSad.query.filter(PostHlaskaSad.user_id == self.id, PostHlaskaSad.hlaska_id == post.id).count() > 0

    def laugh_hlaska_post(self, post):
        if not self.has_laugh_hlaska_post(post):
            laugh = PostHlaskaLaugh(user_id=self.id, hlaska_id=post.id)
            db.session.add(laugh)

    def unlaugh_hlaska_post(self, post):
        if self.has_laugh_hlaska_post(post):
            PostHlaskaLaugh.query.filter_by(
                user_id=self.id,
                hlaska_id=post.id).delete()

    def has_laugh_hlaska_post(self, post):
        return PostHlaskaLaugh.query.filter(PostHlaskaLaugh.user_id == self.id, PostHlaskaLaugh.hlaska_id == post.id).count() > 0

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}', '{self.icanteen}')"


from forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm, PriznaniForm, HlaskaForm, ResetPasswordForm, RequestResetForm


class Priznani(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    picture = db.Column(db.String(20))
    comments = db.relationship('CommentPriznani', backref='article', lazy=True, cascade="all, delete-orphan")
    likes = db.relationship('PostPriznaniLike', backref='priznani', lazy='dynamic')
    loves = db.relationship('PostPriznaniLove', backref='priznani', lazy='dynamic')
    confuses = db.relationship('PostPriznaniConfused', backref='priznani', lazy='dynamic')
    angry = db.relationship('PostPriznaniAngry', backref='priznani', lazy='dynamic')
    surprise = db.relationship('PostPriznaniSurprised', backref='priznani', lazy='dynamic')
    sad = db.relationship('PostPriznaniSad', backref='priznani', lazy='dynamic')
    laugh = db.relationship('PostPriznaniLaugh', backref='priznani', lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(160), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Comment('{self.body}', '{self.date_posted}')"


class CommentPriznani(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(160), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('priznani.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Comment('{self.body}', '{self.date_posted}')"


class CommentHlaska(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(160), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('hlaska.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Comment('{self.body}', '{self.date_posted}')"


class Hlaska(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable=False)
    ucitel = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.relationship('CommentHlaska', backref='article', lazy=True, cascade="all, delete-orphan")
    likes = db.relationship('PostHlaskaLike', backref='hlaska', lazy='dynamic')
    loves = db.relationship('PostHlaskaLove', backref='hlaska', lazy='dynamic')
    confuses = db.relationship('PostHlaskaConfused', backref='hlaska', lazy='dynamic')
    angry = db.relationship('PostHlaskaAngry', backref='hlaska', lazy='dynamic')
    surprise = db.relationship('PostHlaskaSurprised', backref='hlaska', lazy='dynamic')
    sad = db.relationship('PostHlaskaSad', backref='hlaska', lazy='dynamic')
    laugh = db.relationship('PostHlaskaLaugh', backref='hlaska', lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.date_posted, self.ucitel}')"


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    picture = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    jidlo = db.Column(db.String(50), nullable=False)
    comments = db.relationship('Comment', backref='article', lazy=True, cascade="all, delete-orphan")
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    loves = db.relationship('PostLove', backref='post', lazy='dynamic')
    confuses = db.relationship('PostConfused', backref='post', lazy='dynamic')
    angry = db.relationship('PostAngry', backref='post', lazy='dynamic')
    surprise = db.relationship('PostSurprised', backref='post', lazy='dynamic')
    sad = db.relationship('PostSad', backref='post', lazy='dynamic')
    laugh = db.relationship('PostLaugh', backref='post', lazy='dynamic')
    rating_overall = db.Column(db.Integer)
    rating_count = db.Column(db.Integer)
    rating = db.Column(db.String(5))
    ratings = db.relationship('Rating', backref='post_author', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Rating(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    count = db.Column(db.String(10))


class MyModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        elif current_user.email == 'projektjidelna@gmail.com':
            return True
        return False


admin = Admin(app)
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))
admin.add_view(MyModelView(Rating, db.session))
admin.add_view(MyModelView(Comment, db.session))
admin.add_view(MyModelView(Priznani, db.session))
admin.add_view(MyModelView(CommentPriznani, db.session))
admin.add_view(MyModelView(Hlaska, db.session))
admin.add_view(MyModelView(CommentHlaska, db.session))


@app.route('/rate')
@login_required
def rate_meal():
    post_id = request.args.get('post_id')
    stars = request.args.get('stars')
    post = Post.query.filter_by(id=post_id).first_or_404()
    ratings = Rating.query.filter_by(author=current_user)
    current_rating = 0
    for rating in ratings:
        if rating.author == current_user and rating.post_author == post:
            post.rating_overall -= int(rating.count)
            post.rating_count -= 1
            current_rating = str(int(rating.count)/10)
            rating.count = str(int(stars) * 10)
            if int(stars) == 0:
                db.session.delete(rating)
                db.session.commit()
            break
    else:
        if int(stars) != 0:
            rating = Rating(post=post.id, author=current_user, count=str(int(stars)*10))
            db.session.add(rating)
            db.session.commit()

    if post.rating_overall is None:
        post.rating_overall = 0
        post.rating_count = 0

    if int(stars) != 0:
        for counter in range(1, 6):
            if int(stars) == counter:
                html_id = 'input[value=' + stars + str(post.id) + ']'
                post.rating_count += 1
                post.rating_overall += 10 * counter
    else:
        html_id = 'input[value=' + str(int(float(current_rating))) + str(post.id) + ']'

    if post.rating_count != 0:
        post.rating = str(round(post.rating_overall / post.rating_count / 10, 1))
    else:
        post.rating = 0
    db.session.commit()
    return jsonify(html_id=html_id, rating=post.rating, poust_id=post.id)


@app.route('/like')
@login_required
def like_action():
    post_id = request.args.get('post_id')
    action = request.args.get('action')
    this_id = request.args.get('this_id')
    count = request.args.get('count')
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
        div_class = "blue"
        add_or_remove = "add"
        new_text = " " + str(int(count) + 1)
        action = 'unlike'
    else:
        current_user.unlike_post(post)
        db.session.commit()
        div_class = "blue"
        add_or_remove = "remove"
        new_text = " " + str(int(count) - 1)
        action = "like"
    this_id = "#" + str(this_id)
    new_text_id = "#spanlike" + str(post_id)
    return jsonify(this_id=this_id, div_class=div_class, add_or_remove=add_or_remove, new_text=new_text, new_text_id=new_text_id, action=action)


@app.route('/love')
@login_required
def love_action():
    post_id = request.args.get('post_id')
    action = request.args.get('action')
    this_id = request.args.get('this_id')
    count = request.args.get('count')
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'love':
        current_user.love_post(post)
        db.session.commit()
        div_class = "red"
        add_or_remove = "add"
        new_text = " " + str(int(count) + 1)
        action = 'unlove'
    else:
        current_user.unlove_post(post)
        db.session.commit()
        div_class = "red"
        add_or_remove = "remove"
        new_text = " " + str(int(count) - 1)
        action = "love"
    this_id = "#" + str(this_id)
    new_text_id = "#spanlove" + str(post_id)
    return jsonify(this_id=this_id, div_class=div_class, add_or_remove=add_or_remove, new_text=new_text, new_text_id=new_text_id, action=action)


@app.route('/confuse')
@login_required
def confuse_action():
    post_id = request.args.get('post_id')
    action = request.args.get('action')
    this_id = request.args.get('this_id')
    count = request.args.get('count')
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'confuse':
        current_user.confuse_post(post)
        db.session.commit()
        div_class = "yellow-green"
        add_or_remove = "add"
        new_text = " " + str(int(count) + 1)
        action = 'unconfuse'
    else:
        current_user.unconfuse_post(post)
        db.session.commit()
        div_class = "yellow-green"
        add_or_remove = "remove"
        new_text = " " + str(int(count) - 1)
        action = "confuse"
    this_id = "#" + str(this_id)
    new_text_id = "#spanconfuse" + str(post_id)
    return jsonify(this_id=this_id, div_class=div_class, add_or_remove=add_or_remove, new_text=new_text, new_text_id=new_text_id, action=action)


@app.route('/angry')
@login_required
def angry_action():
    post_id = request.args.get('post_id')
    action = request.args.get('action')
    this_id = request.args.get('this_id')
    count = request.args.get('count')
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'angry':
        current_user.angry_post(post)
        db.session.commit()
        div_class = "red-red"
        add_or_remove = "add"
        new_text = " " + str(int(count) + 1)
        action = 'unangry'
    else:
        current_user.unangry_post(post)
        db.session.commit()
        div_class = "red-red"
        add_or_remove = "remove"
        new_text = " " + str(int(count) - 1)
        action = "angry"
    this_id = "#" + str(this_id)
    new_text_id = "#spanangry" + str(post_id)
    return jsonify(this_id=this_id, div_class=div_class, add_or_remove=add_or_remove, new_text=new_text, new_text_id=new_text_id, action=action)


@app.route('/surprise')
@login_required
def surprise_action():
    post_id = request.args.get('post_id')
    action = request.args.get('action')
    this_id = request.args.get('this_id')
    count = request.args.get('count')
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'surprise':
        current_user.surprise_post(post)
        db.session.commit()
        div_class = "yellow-red"
        add_or_remove = "add"
        new_text = " " + str(int(count) + 1)
        action = 'unsurprise'
    else:
        current_user.unsurprise_post(post)
        db.session.commit()
        div_class = "yellow-red"
        add_or_remove = "remove"
        new_text = " " + str(int(count) - 1)
        action = "surprise"
    this_id = "#" + str(this_id)
    new_text_id = "#spansurprise" + str(post_id)
    return jsonify(this_id=this_id, div_class=div_class, add_or_remove=add_or_remove, new_text=new_text, new_text_id=new_text_id, action=action)


@app.route('/sad')
@login_required
def sad_action():
    post_id = request.args.get('post_id')
    action = request.args.get('action')
    this_id = request.args.get('this_id')
    count = request.args.get('count')
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'sad':
        current_user.sad_post(post)
        db.session.commit()
        div_class = "yellow-blue"
        add_or_remove = "add"
        new_text = " " + str(int(count) + 1)
        action = 'unsad'
    else:
        current_user.unsad_post(post)
        db.session.commit()
        div_class = "yellow-blue"
        add_or_remove = "remove"
        new_text = " " + str(int(count) - 1)
        action = "sad"
    this_id = "#" + str(this_id)
    new_text_id = "#spansad" + str(post_id)
    return jsonify(this_id=this_id, div_class=div_class, add_or_remove=add_or_remove, new_text=new_text, new_text_id=new_text_id, action=action)


@app.route('/laugh')
@login_required
def laugh_action():
    post_id = request.args.get('post_id')
    action = request.args.get('action')
    this_id = request.args.get('this_id')
    count = request.args.get('count')
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'laugh':
        current_user.laugh_post(post)
        db.session.commit()
        div_class = "yellow-blue"
        add_or_remove = "add"
        new_text = " " + str(int(count) + 1)
        action = 'unlaugh'
    else:
        current_user.unlaugh_post(post)
        db.session.commit()
        div_class = "yellow-blue"
        add_or_remove = "remove"
        new_text = " " + str(int(count) - 1)
        action = "laugh"
    this_id = "#" + str(this_id)
    new_text_id = "#spanlaugh" + str(post_id)
    return jsonify(this_id=this_id, div_class=div_class, add_or_remove=add_or_remove, new_text=new_text,new_text_id=new_text_id, action=action)


@app.route('/like_priznani/<int:post_id>/<action>')
@login_required
def like_priznani_action(post_id, action):
    post = Priznani.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_priznani_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_priznani_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/love_priznani/<int:post_id>/<action>')
@login_required
def love_priznani_action(post_id, action):
    post = Priznani.query.filter_by(id=post_id).first_or_404()
    if action == 'love':
        current_user.love_priznani_post(post)
        db.session.commit()
    if action == 'unlove':
        current_user.unlove_priznani_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/confuse_priznani/<int:post_id>/<action>')
@login_required
def confuse_priznani_action(post_id, action):
    post = Priznani.query.filter_by(id=post_id).first_or_404()
    if action == 'confuse':
        current_user.confuse_priznani_post(post)
        db.session.commit()
    if action == 'unconfuse':
        current_user.unconfuse_priznani_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/angry_priznani/<int:post_id>/<action>')
@login_required
def angry_priznani_action(post_id, action):
    post = Priznani.query.filter_by(id=post_id).first_or_404()
    if action == 'angry':
        current_user.angry_priznani_post(post)
        db.session.commit()
    if action == 'unangry':
        current_user.unangry_priznani_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/surprise_priznani/<int:post_id>/<action>')
@login_required
def surprise_priznani_action(post_id, action):
    post = Priznani.query.filter_by(id=post_id).first_or_404()
    if action == 'surprise':
        current_user.surprise_priznani_post(post)
        db.session.commit()
    if action == 'unsurprise':
        current_user.unsurprise_priznani_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/sad_priznani/<int:post_id>/<action>')
@login_required
def sad_priznani_action(post_id, action):
    post = Priznani.query.filter_by(id=post_id).first_or_404()
    if action == 'sad':
        current_user.sad_priznani_post(post)
        db.session.commit()
    if action == 'unsad':
        current_user.unsad_priznani_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/laugh_priznani/<int:post_id>/<action>')
@login_required
def laugh_priznani_action(post_id, action):
    post = Priznani.query.filter_by(id=post_id).first_or_404()
    if action == 'laugh':
        current_user.laugh_priznani_post(post)
        db.session.commit()
    if action == 'unlaugh':
        current_user.unlaugh_priznani_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/like_hlaska/<int:post_id>/<action>')
@login_required
def like_hlaska_action(post_id, action):
    post = Hlaska.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_hlaska_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_hlaska_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/love_hlaska/<int:post_id>/<action>')
@login_required
def love_hlaska_action(post_id, action):
    post = Hlaska.query.filter_by(id=post_id).first_or_404()
    if action == 'love':
        current_user.love_hlaska_post(post)
        db.session.commit()
    if action == 'unlove':
        current_user.unlove_hlaska_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/confuse_hlaska/<int:post_id>/<action>')
@login_required
def confuse_hlaska_action(post_id, action):
    post = Hlaska.query.filter_by(id=post_id).first_or_404()
    if action == 'confuse':
        current_user.confuse_hlaska_post(post)
        db.session.commit()
    if action == 'unconfuse':
        current_user.unconfuse_hlaska_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/angry_hlaska/<int:post_id>/<action>')
@login_required
def angry_hlaska_action(post_id, action):
    post = Hlaska.query.filter_by(id=post_id).first_or_404()
    if action == 'angry':
        current_user.angry_hlaska_post(post)
        db.session.commit()
    if action == 'unangry':
        current_user.unangry_hlaska_post(post)
        db.session.commit()
    return redirect(request.referrer)



@app.route('/surprise_hlaska/<int:post_id>/<action>')
@login_required
def surprise_hlaska_action(post_id, action):
    post = Hlaska.query.filter_by(id=post_id).first_or_404()
    if action == 'surprise':
        current_user.surprise_hlaska_post(post)
        db.session.commit()
    if action == 'unsurprise':
        current_user.unsurprise_hlaska_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/sad_hlaska/<int:post_id>/<action>')
@login_required
def sad_hlaska_action(post_id, action):
    post = Hlaska.query.filter_by(id=post_id).first_or_404()
    if action == 'sad':
        current_user.sad_hlaska_post(post)
        db.session.commit()
    if action == 'unsad':
        current_user.unsad_hlaska_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/laugh_hlaska/<int:post_id>/<action>')
@login_required
def laugh_hlaska_action(post_id, action):
    post = Hlaska.query.filter_by(id=post_id).first_or_404()
    if action == 'laugh':
        current_user.laugh_hlaska_post(post)
        db.session.commit()
    if action == 'unlaugh':
        current_user.unlaugh_hlaska_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route("/")
def home():
    if current_user.is_authenticated:
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=1, per_page=2)
        now = datetime.now()
        now_time = now.time()
        if datetime.today().weekday() == 4:
            kolik_je = "Pondělní obědy:"
            counter = 1
        elif datetime.today().weekday() == 5:
            kolik_je = "Pondělní obědy:"
            counter = 0
        elif datetime.today().weekday() == 6:
            kolik_je = "Zítřejší obědy:"
            counter = 0
        elif now_time > time(15, 00):
            kolik_je = r"Zítřejší obědy:"
            counter = 1
        else:
            kolik_je = "Dnešní obědy:"
            counter = 0
        return render_template('home.html', posts=posts,  dnesni_jidla=dnesni_jidla(), link="home", counter=counter, kolik_je=kolik_je, vybrane_jidla_mesic=vybrane_jidla_mesic())
    else:
        return render_template('not_registered.html')


@app.route("/jidla")
@login_required
def jidla():
    posts = Post.query.order_by(Post.date_posted.desc())
    now = datetime.now()
    now_time = now.time()
    if now_time < time(11, 30) or (datetime.today().weekday() == 5 or datetime.today().weekday() == 6):
        cas = 0
    else:
        cas = 1
    ratings = Rating.query.filter_by(author=current_user)
    return render_template('vybrani_jidel.html', meals=get_jidla(), link="jidla", vybrane_jidla_mesic=vybrane_jidla_mesic(), posts=posts, cas=cas, title="Projekt Jídelna - Výběr jídel", ratings=ratings)


@app.route("/vyber_jidel", methods=['GET', 'POST'])
@login_required
def vyber_jidel():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.53'
    }
    login_data = {
        'j_username': current_user.icanteen,
        'j_password': current_user.icanteen_heslo,
        'terminal': 'false',
        'type': 'web',
        '_spring_security_remember_me': "on"
    }
    with requests.session() as session:
        url = 'https://jidelna.mgo.opava.cz:6204/faces/login.jsp'
        r = session.get(url)
        soup = bs4.BeautifulSoup(r.content, features="html.parser")
        login_data['_csrf'] = soup.find('input', attrs={'name': '_csrf'})['value']
        login_data['targetUrl'] = soup.find('input', attrs={'name': 'targetUrl'})['value']
        r = session.post('https://jidelna.mgo.opava.cz:6204/j_spring_security_check', data=login_data, headers=headers)
        r = session.get('https://jidelna.mgo.opava.cz:6204/faces/secured/mobile.jsp')
    soup = bs4.BeautifulSoup(r.content, features="html.parser")
    vybrane_jidla = []
    chosen = True
    for den in soup.select('#mainContext tr'):
        if not chosen:
            vybrane_jidla.append(0)
        chosen = False
        counter = 1
        dalsi_den = den.select('div .jidelnicekItem')
        for div in dalsi_den:
            jidlo = div.select('.fa-2x')
            if jidlo:
                vybrane_jidla.append(counter)
                chosen = True
            counter += 1
    try:
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path="./static/geckodriver.exe", options=options)
    except:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(executable_path="./static/chromedriver.exe", options=options)

    driver.get("https://jidelna.mgo.opava.cz:6204/faces/login.jsp")
    nameElem = driver.find_elements_by_class_name('form-control')[0]
    nameElem.send_keys(current_user.icanteen)
    passwordElem = driver.find_elements_by_class_name('form-control')[1]
    passwordElem.send_keys(current_user.icanteen_heslo)
    passwordElem.submit()
    sleep(.8)
    mesic = driver.find_elements_by_class_name('mainMenu')[2]
    mesic.click()
    now = datetime.now()
    now_time = now.time()
    counter = 3
    for i in range(1, 35):
        string = 'group' + str(i)
        vybrane_jidlo_ = request.form.get(string)
        if vybrane_jidlo_ is not None and int(vybrane_jidlo_) != vybrane_jidla[i] and int(vybrane_jidlo_) != 4:
            jidlo = driver.find_elements_by_css_selector('.btn.button-link.button-link-main')[counter + int(vybrane_jidlo_)-1]  # 6 == 3. den 1. oběd

            try:
                jidlo.click()
            except Exception as e:
                print(e)
            sleep(.5)
        elif vybrane_jidlo_ is not None and int(vybrane_jidlo_) == 4:
            if vybrane_jidla[i] != 0:
                jidlo = driver.find_elements_by_css_selector('.btn.button-link.button-link-main')[counter + vybrane_jidla[i]-1]
                try:
                    jidlo.click()
                except Exception as e:
                    print(e)
                sleep(1)

        counter += 3
    flash('Tvoje obědy jsou nyní uloženy.', 'success')
    driver.close()
    return redirect(request.referrer)


@app.route('/comment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.content.data, post_id=post_id, author=current_user)
        db.session.add(comment)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/comment/<int:comment_id>/delete')
@login_required
def delete_comment(comment_id):
    commentD = Comment.query.get_or_404(comment_id)
    if current_user == commentD.author:
        db.session.delete(commentD)
        db.session.commit()
        flash('Tvůj komentář byl smazán!', 'success')
    return redirect(request.referrer)


@app.route('/comment_priznani/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comment_priznani(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = CommentPriznani(body=form.content.data, post_id=post_id, author=current_user)
        db.session.add(comment)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/comment_priznani/<int:comment_id>/delete')
@login_required
def delete_comment_priznani(comment_id):
    commentD = CommentPriznani.query.get_or_404(comment_id)
    if current_user == commentD.author:
        db.session.delete(commentD)
        db.session.commit()
        flash('Tvůj komentář byl smazán!', 'success')
    return redirect(request.referrer)


@app.route('/comment_hlaska/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comment_hlaska(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = CommentHlaska(body=form.content.data, post_id=post_id, author=current_user)
        db.session.add(comment)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/comment_hlaska/<int:comment_id>/delete')
@login_required
def delete_comment_hlaska(comment_id):
    commentE = CommentHlaska.query.get_or_404(comment_id)
    if current_user == commentE.author:
        db.session.delete(commentE)
        db.session.commit()
        flash('Tvůj komentář byl smazán!', 'success')
    return redirect(request.referrer)


@app.route('/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash('Tvoje recenze byla smazána!', 'success')
    return redirect(request.referrer)


@app.route('/hlaska/<int:post_id>/delete')
@login_required
def delete_hlaska(post_id):
    post = Hlaska.query.get_or_404(post_id)
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash('Tvoje hláška byla smazáno!', 'success')
    return redirect(request.referrer)


@app.route("/recenze", methods=['GET', 'POST'])
@login_required
def recenze():
    form = PostForm()
    commentForm = CommentForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 1500, 1500)
        post = Post(title=form.title.data, content=form.content.data, author=current_user, picture=picture_file, jidlo=form.jidlo.data, rating="X.x")
        db.session.add(post)
        db.session.commit()
        flash('Tvůj přispěvek byl vytvořen', 'success')
        posts = Post.query.filter_by(author=current_user)
        counter = 0
        for post in posts:
            counter += 1
        if counter >= 100:
            current_user.diamondUser = 1
            db.session.commit()
        elif counter >= 50:
            current_user.platinumUser = 1
            db.session.commit()
        elif counter >= 25:
            current_user.goldUser = 1
            db.session.commit()
        elif counter >= 10:
            current_user.silverUser = 1
            db.session.commit()
        elif counter >= 5:
            current_user.bronzeUser = 1
            db.session.commit()
        return redirect(url_for('.recenze'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    comments = Comment.query.all()
    ratings = Rating.query.filter_by(author=current_user)
    return render_template('recenze.html', title='Projekt Jídelna - Recenze', form=form, link="recenze", posts=posts, comments=comments, commentForm=commentForm, ratings=ratings)


@app.route("/search")
def search():
    form = PostForm()
    hledane_jidlo = request.args.get('search').lower()
    hledane_jidlo_s_jinym_kodovanim = unicodedata.normalize('NFKD', hledane_jidlo)
    hledane_jidlo_bez_diaktritiky = ""
    for pismeno in hledane_jidlo_s_jinym_kodovanim:
        if not unicodedata.combining(pismeno):
            hledane_jidlo_bez_diaktritiky += pismeno
    jidlo_regex = re.compile(hledane_jidlo_bez_diaktritiky)
    posts = Post.query.order_by(Post.date_posted.desc())
    vyhledane_posty = []
    for post in posts:
        jidlo_z_post_bez_diaktritiky = ""
        jidlo_z_post_s_jinym_kodovanim = unicodedata.normalize('NFKD', post.jidlo.lower())
        for letter in jidlo_z_post_s_jinym_kodovanim:
            if not unicodedata.combining(letter):
                jidlo_z_post_bez_diaktritiky += letter
        if jidlo_regex.search(jidlo_z_post_bez_diaktritiky) is not None:
            vyhledane_posty.append(post)

    commentForm = CommentForm()
    comments = Comment.query.all()
    return render_template("search.html", posts=vyhledane_posty, comments=comments, commentForm=commentForm, link="search", form=form)


@app.route("/priznani", methods=['GET', 'POST'])
@login_required
def priznani():
    form = PriznaniForm()
    commentForm = CommentForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 1500, 1500)
        else:
            picture_file = ""
        post = Priznani(content=form.content.data, picture=picture_file)
        db.session.add(post)
        db.session.commit()
        flash('Tvoje přiznání byl vytvořen', 'success')
        return redirect(url_for('.priznani'))
    page = request.args.get('page', 1, type=int)
    posts = Priznani.query.order_by(Priznani.date_posted.desc()).paginate(page=page, per_page=6)
    comments = CommentPriznani.query.all()
    return render_template('priznani.html', title='Přiznání MGO', form=form, link="priznani", posts=posts, comments=comments, commentForm=commentForm)


@app.route("/kontakt")
def about():
    return render_template('about.html', title="Projekt Jídelna - Kontakt", link="about")


@app.route("/hlasky", methods=['GET', 'POST'])
@login_required
def hlasky():
    form = HlaskaForm()
    if form.validate_on_submit():
        post = Hlaska(content=form.content.data, ucitel=form.ucitel.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Tvoje hláška byla přidána', 'success')
        return redirect(url_for('.hlasky'))
    commentForm = CommentForm()
    page = request.args.get('page', 1, type=int)
    posts = Hlaska.query.order_by(Hlaska.date_posted.desc()).paginate(page=page, per_page=6)
    comments = CommentHlaska.query.all()
    return render_template('hlasky.html', title="Hlášky učitelů", form=form, link="hlasky", posts=posts, comments=comments, commentForm=commentForm)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.jidelna.data and form.jidelna_heslo.data:
            user = User(name=form.name.data, email=form.email.data, password=password, icanteen=form.jidelna.data, icanteen_heslo=form.jidelna_heslo.data)
        else:
            user = User(name=form.name.data, email=form.email.data, password=password)
        db.session.add(user)
        db.session.commit()
        flash(f'Účet byl vytvořen!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Projekt Jídelna - Registrace', form=form, link="register")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Nyní jsi přihlášený jako ' + user.name + ".", 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Přihlášení se nezdařilo. Zkontroluj si přezdívku a heslo.', 'danger')
    return render_template('login.html', title='Projekt Jídelna - Přihlášení', form=form, link="login")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('.home'))


def save_picture(form_picture, width, height):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (width, height)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/ucet", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 500, 500)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.icanteen = form.jidelna.data
        current_user.icanteen_heslo = form.jidelna_heslo.data
        db.session.commit()
        flash('Tvůj účet byl aktualizován!', 'success')
        return redirect(url_for('.account'))
    if request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.jidelna.data = current_user.icanteen
        form.jidelna_heslo.data = current_user.icanteen_heslo
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Projekt Jídelna - Účet', image_file=image_file, form=form, link="account")


@app.route("/search_ucitel")
def search_ucitel():
    form = HlaskaForm()
    hledane_jidlo = request.args.get('ucitel')
    if hledane_jidlo == "":
        return redirect(url_for('.hlasky'))
    jidlo_regex = re.compile(hledane_jidlo)
    posts = Hlaska.query.all()
    vyhledane_posty = []
    for post in posts:
        if jidlo_regex.search(post.ucitel) is not None:
            vyhledane_posty.append(post)

    commentForm = CommentForm()
    comments = CommentHlaska.query.all()
    return render_template("search_ucitel.html", posts=vyhledane_posty, comments=comments, commentForm=commentForm, link="search", current_ucitel=hledane_jidlo, form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Změna hesla', sender='projektjidelna@gmail.com', recipients=[user.email])
    msg.body = f'''
Pro resetování hesla klikni na následující odkaz:
{url_for('reset_token', token=token, _external=True)}
Pokud jste si nevyžádali tento email, jednoduše neprovádějte žádnou akci.
               '''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Poslali jsme ti email s instrukcemi', 'success')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Projekt Jídelna - změna hesla', form=form, link='login')


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_secret_token(token)
    if user is None:
        flash('Tento token je buď nesprávný nebo mu vypršela platnost', 'danger')
        return redirect(url_for('.reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = password
        db.session.commit()
        flash(f'Tvoje heslo bylo změněno!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Projekt Jídelna - změna hesla', form=form, link='login')


@app.route("/html")
def html():
    return render_template('html.html', title='HTML Tagy', link='tutorial')


def get_jidla():
    jidla = []

    try:
        url = requests.get('https://jidelna.mgo.opava.cz:6204/faces/login.jsp')
        url.raise_for_status()
        soup = bs4.BeautifulSoup(url.text, features="html.parser")

        jidelnicek_datum = soup.select('div .jidelnicekDen div strong .important')  # list datumů
        jidelnicek_den = soup.select('div .jidelnicekDen div strong span')  # list dnů v týdnu
        jidelnicek_jidlo = soup.select('div .jidelnicekDen div div')

        dny = {}

        for datum in jidelnicek_datum:
            text2 = datum.text
            dny[text2.strip()] = ""  # Vytvoří key v listu dny

        dnyvtydnu = []
        for den in jidelnicek_den:
            text3 = den.text
            if re.match('^[P, Ú, S, Č, P]+', text3.strip()) is not None:
                dnyvtydnu.append(text3.strip())

        counter = 0
        for i in dny.keys():
            dny[i] = dnyvtydnu[counter]  # Přidá k datům názvy dnů
            counter += 1

        jidlo = []
        for i in jidelnicek_jidlo:
            split_text = i.text.split('                    ')
            jidlo.append(split_text[0].strip())
            jidlo.append(split_text[5].strip())  # Jídla

        counter = 0
        remove_first_two_meals = 0
        now = datetime.now()
        now_time = now.time()
        if now_time < time(11, 30) or (datetime.today().weekday() == 5 or datetime.today().weekday() == 6):
            prvni_den_ven = 0
        else:
            prvni_den_ven = 1
        for keys, values in dny.items():
            if remove_first_two_meals > prvni_den_ven:
                jidla.append(values + " - " + keys)
            if jidlo[counter].startswith("Oběd 1"):
                if remove_first_two_meals > prvni_den_ven:
                    jidla.append("A" + jidlo[counter + 1])
                counter += 2
            if jidlo[counter].startswith("Oběd 2"):
                if remove_first_two_meals > prvni_den_ven:
                    jidla.append("B" + jidlo[counter + 1])
                counter += 2
            if jidlo[counter].startswith("Oběd 3"):
                if remove_first_two_meals > prvni_den_ven:
                    jidla.append("C" + jidlo[counter + 1])
                counter += 2
            remove_first_two_meals += 1
        return jidla
    except requests.exceptions.ConnectionError:
        return None;


def dnesni_jidla():
    now = datetime.now()
    now_time = now.time()
    if current_user.icanteen or ((datetime.today().weekday() == 4 and current_user.icanteen) or (datetime.today().weekday() == 5 and current_user.icanteen) or (datetime.today().weekday() == 6 and current_user.icanteen)):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.53'
        }
        login_data = {
            'j_username': current_user.icanteen,
            'j_password': current_user.icanteen_heslo,
            'terminal': 'false',
            'type': 'web',
            '_spring_security_remember_me': "on"
        }
        with requests.session() as session:
            url = 'https://jidelna.mgo.opava.cz:6204/faces/login.jsp'

            r = session.get(url)
            soup = bs4.BeautifulSoup(r.content, features="html.parser")
            login_data['_csrf'] = soup.find('input', attrs={'name': '_csrf'})['value']
            login_data['targetUrl'] = soup.find('input', attrs={'name': 'targetUrl'})['value']

            r = session.post('https://jidelna.mgo.opava.cz:6204/j_spring_security_check', data=login_data, headers=headers)
            soup = bs4.BeautifulSoup(r.content, features="html.parser")
            bad_credential = re.compile(r'Bad credentials')
            not_logged = bad_credential.search(soup.text)
            if not_logged is None:
                if datetime.today().weekday() == 4:
                    tomorrow = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
                elif datetime.today().weekday() == 5:
                    tomorrow = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
                elif datetime.today().weekday() == 6:
                    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
                elif now_time > time(15, 00):
                    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
                else:
                    tomorrow = datetime.now().strftime('%Y-%m-%d')
                response = session.get('https://jidelna.mgo.opava.cz:6204/faces/secured/mobile.jsp')
                soup = bs4.BeautifulSoup(response.content, features="html.parser")
                zitra = soup.select('#orderContent%s .jidelnicekItem span > span:nth-of-type(2)' % tomorrow)
                jidla_zitra = []
                for jidlo in zitra:
                    " ".join(jidlo.text.split())
                    jidla_zitra.append(" ".join(jidlo.text.split()))
                if jidla_zitra:
                    if len(jidla_zitra) == 1:
                        jidla_zitra.append("TENTO OBĚD SE DNESKA NEVAŘÍ TENTO OBĚD SE DNESKA NEVAŘÍ")
                        jidla_zitra.append("TENTO OBĚD SE DNESKA NEVAŘÍ TENTO OBĚD SE DNESKA NEVAŘÍ")
                    elif len(jidla_zitra) == 2:
                        jidla_zitra.append("TENTO OBĚD SE DNESKA NEVAŘÍ TENTO OBĚD SE DNESKA NEVAŘÍ")
                    return jidla_zitra
                else:
                    try:
                        url = requests.get('https://jidelna.mgo.opava.cz:6204/faces/login.jsp')
                        url.raise_for_status()

                        soup = bs4.BeautifulSoup(url.text, features="html.parser")

                        jidelnicek_jidlo = soup.select('div .jidelnicekDen div div')

                        jidlo = []

                        for i in range(3):
                            jidlo.append(jidelnicek_jidlo[i].text.split('                    ')[5].strip())

                        dates = soup.select(
                            'div #day-%s span' % strftime("%Y-%m-%d", gmtime()))  # list divu s dnešním datem

                        if not dates:
                            return [
                                "TENTO OBĚD SE DNESKA NEVAŘÍ TENTO OBĚD SE DNESKA NEVAŘÍ",
                                "TENTO OBĚD SE DNESKA NEVAŘÍ TENTO OBĚD SE DNESKA NEVAŘÍ",
                                "TENTO OBĚD SE DNESKA NEVAŘÍ TENTO OBĚD SE DNESKA NEVAŘÍ"
                            ]

                        return jidlo
                    except requests.exceptions.ConnectionError:
                        return None;
            else:
                return ["Nejspíš máš špatně zadané iCanteenID nebo iCanteen heslo", "Je však taky možné, že spadly jídelně servery", "Zkontroluj zady: https://jidelna.mgo.opava.cz: 6204/faces/login.jsp"]
    else:
        return ["Nejspíš máš špatně zadané iCanteenID nebo iCanteen heslo", "Je však taky možné, že spadly jídelně servery", "Zkontroluj zady: https://jidelna.mgo.opava.cz: 6204/faces/login.jsp"]


def vybrane_jidlo():
    if current_user.icanteen != "":
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.53'
        }

        login_data = {
            'j_username': current_user.icanteen,
            'j_password': current_user.icanteen_heslo,
            'terminal': 'false',
            'type': 'web',
            '_spring_security_remember_me': "on"
        }

        with requests.session() as session:
            url = 'https://jidelna.mgo.opava.cz:6204/faces/login.jsp'

            r = session.get(url)
            soup = bs4.BeautifulSoup(r.content, features="html.parser")
            login_data['_csrf'] = soup.find('input', attrs={'name': '_csrf'})['value']
            login_data['targetUrl'] = soup.find('input', attrs={'name': 'targetUrl'})['value']

            r = session.post('https://jidelna.mgo.opava.cz:6204/j_spring_security_check', data=login_data, headers=headers)

            now = datetime.now()
            now_time = now.time()
            if now_time > time(15, 00):
                r = session.get('https://jidelna.mgo.opava.cz:6204/faces/secured/mobile.jsp')

        soup = bs4.BeautifulSoup(r.content, features="html.parser")
        vybrane_jidlo = soup.select('div .jidelnicekItem')
        counter = 0
        for div in vybrane_jidlo:
            counter += 1
            jidlo = div.select('.fa-2x')
            if jidlo:
                break
        return counter
    else:
        return 0


def vybrane_jidla_mesic():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.53'
    }
    login_data = {
        'j_username': current_user.icanteen,
        'j_password': current_user.icanteen_heslo,
        'terminal': 'false',
        'type': 'web',
        '_spring_security_remember_me': "on"
    }
    with requests.session() as session:
        url = 'https://jidelna.mgo.opava.cz:6204/faces/login.jsp'
        r = session.get(url)
        soup = bs4.BeautifulSoup(r.content, features="html.parser")
        login_data['_csrf'] = soup.find('input', attrs={'name': '_csrf'})['value']
        login_data['targetUrl'] = soup.find('input', attrs={'name': 'targetUrl'})['value']
        r = session.post('https://jidelna.mgo.opava.cz:6204/j_spring_security_check', data=login_data, headers=headers)
        r = session.get('https://jidelna.mgo.opava.cz:6204/faces/secured/mobile.jsp')
    soup = bs4.BeautifulSoup(r.content, features="html.parser")
    vybrane_jidla = []
    chosen = True
    for den in soup.select('#mainContext tr'):
        if not chosen:
            vybrane_jidla.append(0)
        chosen = False
        counter = 1
        dalsi_den = den.select('div .jidelnicekItem')
        for div in dalsi_den:
            jidlo = div.select('.fa-2x')
            if jidlo:
                vybrane_jidla.append(counter)
                chosen = True
            counter += 1
    return vybrane_jidla


if __name__ == '__main__':
    app.run(debug=True)
# set FLASK_APP=main.py
