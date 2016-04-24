from flask import Blueprint, render_template, abort, Flask, request, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
import json
from flask.ext.jsonpify import jsonify

level = Flask(__name__)
level.config.from_object('level.config')
db = SQLAlchemy(level)
from level import models
from level.models import *
level = Blueprint('level', 'level')

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

def find_level(name):
    level = Level.query.filter_by(name=name).first()
    return level

def delete_all_users(username):
    users = User.query.all()
    for user in users:
        db.session.delete(user)
    db.session.commit()

#========================= Routes are defined below =======================#

@level.route('/', defaults={'page': 'index'})
def module_name(page):
    return 'level module'

@level.route('/users', methods=["GET"])
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

@level.route('/user/<page>', methods=["GET"])
def show_user(page):
    user = find_user_force(page)
    msg_fail = 'No level'
    level = {'name' : [msg_fail]}
    try:
        level = Level.query.filter_by(points<user.points).order_by(desc(points))[0]
    except:
        pass

    data = ({
        'id': user.id,
        'name': user.nickname,
        'level': level['name']
    })
    return jsonify({
        'success': True,
        'message': 'User exist',
        'data': data
    })

@level.route('/create', methods=["POST"])
def create_level():
    try:
        level = Level(request.form['name'], request.form['description'], request.form['image_name'])
        db.session.add(level)
        db.session.commit()
    except:
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })
    return jsonify({
        'success': True,
        'message': 'level added successfully'
    })

@level.route('/list', methods=["GET"])
def show_all_level():
    level = Level.query.all()
    data = []
    for level in level:
        data.append(level.to_dict())
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })


@level.route('/award', methods=["POST"])
def create_level_user_mapping():
    try:
        user = find_user_force(request.form['username'])
        level = find_level(request.form['level'])
        existing = UserLevel.query.filter_by(user_id=user.id, level_id=level.id).all()
        if len(existing) > 0:
            return jsonify({
                'success': False,
                'message': 'User already has this level'
            })
        mapping = UserLevel(user, level)
        db.session.add(mapping)
        db.session.commit()
    except:
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })
    return jsonify({
        'success': True,
        'message': 'level awarded successfully'
    })

@level.route('/static/<page>', methods=["GET"])
def send_static(page):
    return send_from_directory('level/static', page)
