import flask

from icy_server.main.views import main_blueprint

app = flask.Flask(__name__, template_folder="main/templates", static_folder="main/static")

app.register_blueprint(main_blueprint)

