from flask import Flask
import importlib
from flask.ext.autodoc import Autodoc
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)

# automatic documentation generation
# auto = Autodoc(app)

# Badges registering
from badges import badges
app.register_blueprint(badges, url_prefix='/badges')

# Leaderboard registering
from leaderboard import leaderboard
app.register_blueprint(leaderboard, url_prefix='/leaderboard')

# Avatar registering
from avatar import avatar
app.register_blueprint(avatar, url_prefix='/avatar')

# @app.route('/documentation')
# def documentation():
#     return auto.html()

app.run(debug=True)