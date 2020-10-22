import os

from icy.server import app


LOCALHOST: str = "0.0.0.0"


def main():
    try:
        environment = os.environ.get("FLASK_ENV", "production").lower()
        application_port = int(os.environ.get("FLASK_PORT", 8080))
        if environment == "production":
            from gevent.pywsgi import WSGIServer

            print("Start serving on ", f"{LOCALHOST}:{application_port}")
            serving_location = (LOCALHOST, application_port)
            http_server = WSGIServer(serving_location, app)
            http_server.serve_forever()
        else:
            app.run(host=LOCALHOST, port=application_port)
    except KeyboardInterrupt:
        print("Serving stopped")


main()
