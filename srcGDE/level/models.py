from . import db
# Documentation : http://flask-sqlalchemy.pocoo.org/2.1/
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    points=db.Column(db.Integer,default=0)

    def __init__(self, nickname):
        self.nickname = nickname

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))
    req_points = db.Column(db.Integer)

    def __init__(self, name, description, image_name):
        self.name = name
        self.description = description
        self.req_points = req_points

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'req_points': self.req_points
        }
