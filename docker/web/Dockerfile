FROM python:3.8-slim

COPY ./app /usr/src/app
COPY ./classifier /usr/src/classifier

RUN python -m pip install /usr/src/classifier --no-cache-dir && \
    python -m pip install -r /usr/src/app/requirements.txt --no-cache-dir

ENTRYPOINT [ "python", "/usr/src/app/__main__.py"]
