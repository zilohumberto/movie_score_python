FROM python:3.7.3

ENV PYTHONPATH /opt/web-socket/

RUN mkdir -p /opt/web-socket/
ADD . /opt/web-socket/
WORKDIR /opt/web-socket/
RUN pip install -r requirements.txt
