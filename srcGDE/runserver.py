from flask import Flask
import importlib
from flask.ext.autodoc import Autodoc

app = Flask(__name__)

# automatic documentation generation
# auto = Autodoc(app)

# Badges registering
from badges import badges
app.register_blueprint(badges, url_prefix='/badges')

# Leaderboard registering
from leaderboard import leaderboard
app.register_blueprint(leaderboard, url_prefix='/leaderboard')

# @app.route('/documentation')
# def documentation():
#     return auto.html()

app.run(debug=True)