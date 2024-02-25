FROM python:alpine

COPY . /home/ace
COPY requirements /home/requirements

RUN apk add --no-cache docker bash && \
    pip3 install -r /home/requirements

WORKDIR /home/ace

ENTRYPOINT ["python3", "main.py"]