import functools
import os
from typing import Any, Callable

import redis
import rq


@functools.lru_cache()
def acquire_job_queue() -> rq.Queue:
    redis_host = os.environ.get("REDIS_HOST", "0.0.0.0")
    redis_port = int(os.environ.get("REDIS_PORT", 6379))
    redis_connection = redis.Redis(redis_host, redis_port)
    return rq.Queue(connection=redis_connection)


def submit_task(function: Callable[..., Any], *args, **kwargs):
    jqueue = acquire_job_queue()
    job = jqueue.enqueue(function, *args, **kwargs)
    return job.get_id()
