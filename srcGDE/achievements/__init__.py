from flask import Blueprint, render_template, abort, Flask, request, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
import json
from flask.ext.jsonpify import jsonify

achievement = Flask(__name__)
achievement.config.from_object('achievements.config')
db = SQLAlchemy(achievement)
from achievements import models
from achievements.models import *
achievements = Blueprint('achievements', 'achievements')

#========= The above part will be more or less the same for all GDE =======#

#========================= Non-route functions ============================#

def add_user(username):
    me = User(username)
    db.session.add(me)
    db.session.commit()
    return

def find_user_force(username):
    user = User.query.filter_by(nickname=username).first()
    if user is None:
        add_user(username)
        user = User.query.filter_by(nickname=username).first()
    return user

def find_achievement(name):
    achievement = Achievement.query.filter_by(name=name).first()
    return achievement

def delete_all_users(username):
    users = User.query.all()
    for user in users:
        db.session.delete(user)
    db.session.commit()

#========================= Routes are defined below =======================#

@achievements.route('/', defaults={'page': 'index'})
def module_name(page):
    return 'Achievements module'

@achievements.route('/users', methods=["GET"])
def show_all_users():
    users = User.query.all()
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'name': user.nickname
        })
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

@achievements.route('/user/<page>', methods=["GET"])
def show_user(page):
    user = User.query.filter_by(nickname=page).first()
    achievement_ids = UserAchievement.query.filter_by(user_id=user.id)
    achievements = []
    ach=[]
    for b in achievement_ids:
        ach.append(b.achievement_id)
        achievement = Achievement.query.filter_by(id=b.achievement_id).first()
        achievements.append(achievement.to_dict())

    achievementss = Achievement.query.all()
    all_achievements=[]

    for achievement in achievementss:
        print
        print
        print achievement.to_dict()["id"]
        print achievement_ids
        if achievement.to_dict()["id"] in ach:
            k=1
        else:
            k=0
        temp_dict = achievement.to_dict()
        temp_dict['k'] = k
        all_achievements.append(temp_dict)
    data = ({
        'id': user.id,
        'name': user.nickname,
        'all_achievements':all_achievements
    })
    return jsonify({
        'success': True,
        'message': 'User exist',
        'data': data
    })

@achievements.route('/create', methods=["POST"])
def create_achievement():
    try:
        achievement = Achievement(request.form['name'], request.form['description'], request.form['image_name'])
        db.session.add(achievement)
        db.session.commit()
    except:
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })
    return jsonify({
        'success': True,
        'message': 'Achievement added successfully'
    })

@achievements.route('/list', methods=["GET"])
def show_all_achievements():
    achievements = Achievement.query.all()
    data = []
    for achievement in achievements:
        data.append(achievement.to_dict())
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })


@achievements.route('/award', methods=["POST"])
def create_achievement_user_mapping():
    try:
        user = find_user_force(request.form['username'])
        achievement = find_achievement(request.form['achievement'])
        existing = UserAchievement.query.filter_by(user_id=user.id, achievement_id=achievement.id).all()
        if len(existing) > 0:
            return jsonify({
                'success': False,
                'message': 'User already has this achievement'
            })
        mapping = UserAchievement(user, achievement)
        db.session.add(mapping)
        db.session.commit()
    except:
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })
    return jsonify({
        'success': True,
        'message': 'Achievement awarded successfully'
    })

@achievements.route('/static/<page>', methods=["GET"])
def send_static(page):
    return send_from_directory('achievements/static', page)