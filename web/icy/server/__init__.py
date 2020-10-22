import flask

from icy.server.views import main_blueprint


app = flask.Flask(__name__)
app.register_blueprint(main_blueprint)
