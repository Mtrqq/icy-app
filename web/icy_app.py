from functools import lru_cache
import time
import os

import flask
import rq
import redis

from classifier import recognize_image, list_available_models

app = flask.Flask(__name__)


@lru_cache()
def acquire_job_queue() -> rq.Queue:
    redis_host = os.environ.get("REDIS_HOST", "0.0.0.0")
    redis_port = int(os.environ.get("REDIS_PORT", 6379))
    redis_connection = redis.Redis(redis_host, redis_port)
    return rq.Queue(connection=redis_connection)


@app.route("/")
def index():
    return flask.render_template("index.html.j2", models=list_available_models())


@app.route("/analyse", methods=["POST"])
def analyse_image():
    image_url = flask.request.form["image_url"]
    selected_model = flask.request.form["model"]
    job_queue = acquire_job_queue()
    job = job_queue.enqueue(recognize_image, image_url, selected_model, stringify_labels=True)
    while not (job.is_finished or job.is_failed):
        time.sleep(1)
    if not job.result:
        return f"Job failed due to an exception: {job.exc_info}"
    return flask.jsonify(job.result)
