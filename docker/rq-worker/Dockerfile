FROM python:3.8-slim

WORKDIR /usr/src/rq-worker/

COPY ./torch-gpu.txt ./
COPY ./torch-cpu.txt ./

ARG TORCH_MODE=cpu

RUN python -m pip install -r ./torch-${TORCH_MODE}.txt --no-cache-dir

COPY ./classifier /usr/src/classifier
COPY ./requirements.txt ./

RUN python -m pip install /usr/src/classifier --no-cache-dir && \
    python -m pip install -r ./requirements.txt --no-cache-dir

COPY ./run_worker.py ./run_worker.py
ENTRYPOINT [ "python", "run_worker.py" ]