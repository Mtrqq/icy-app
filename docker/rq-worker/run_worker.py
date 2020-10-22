import os

from redis import Redis
from redis.exceptions import ConnectionError
from rq import Worker

# import to cache package importing
import icy.classifier  # noqa


LOCALHOST: str = "0.0.0.0"


def main():
    host = os.environ.get("REDIS_HOST", LOCALHOST)
    port = int(os.environ.get("REDIS_PORT", 6379))
    worker_ttl = int(os.environ.get("RQ_WORKER_TTL", 600))
    try:
        connection = Redis(host, port)
        worker = Worker(["default"], connection=connection, default_worker_ttl=worker_ttl)
        worker.work()
    except ConnectionError as error:
        raise RuntimeError("Unable to establish redis connection") from error


if __name__ == "__main__":
    main()
