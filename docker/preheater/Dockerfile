# TODO: should be inherited from icy-rq-worker
FROM python:3.8-slim

WORKDIR /usr/src/rq-worker/

COPY ./torch-cpu.txt ./

RUN python -m pip install -r ./torch-cpu.txt --no-cache-dir

COPY ./classifier /usr/src/classifier

RUN python -m pip install /usr/src/classifier --no-cache-dir

COPY ./preheat.py ./preheat.py
ENTRYPOINT [ "python", "preheat.py" ]