FROM python:3.6-alpine


COPY access.py /zelkova/api/access.py
COPY finite_difference.py /zelkova/api/finite_difference.py
COPY first_parser.py /zelkova/api/first_parser.py
COPY influx_logger.py /zelkova/api/influx_logger.py
COPY login_action.py /zelkova/api/login_action.py
COPY pde_parser.py /zelkova/api/pde_parser.py
COPY startup.sh /zelkova/api/startup.sh
COPY mongo_logger.py /zelkova/api/mongo_logger.py




RUN apk add --no-cache bash build-base curl && pip3 install --upgrade pip &&\
    pip3 install gunicorn gunicorn Flask influxdb numpy pymongo requests && chmod +x /zelkova/api/startup.sh

WORKDIR /zelkova/api


