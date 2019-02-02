FROM python:3.6-alpine


COPY pde_parser.py /zelkova/api/pde_parser.py
COPY finite_difference.py /zelkova/api/finite_difference.py
COPY login_action.py /zelkova/api/login_action.py
COPY first_parser.py /zelkova/api/first_parser.py
COPY access.py /zelkova/api/access.py



RUN apk add --no-cache bash build-base  && pip3 install --upgrade pip &&\
	pip3 install gunicorn gunicorn Flask influxdb numpy requests

WORKDIR /zelkova/api


