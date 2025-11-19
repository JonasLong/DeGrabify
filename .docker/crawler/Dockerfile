FROM python:3

ENV SCRIPT_ROOT=/var/www
ENV DB_PATH=/data/sites.json

RUN apt-get update
RUN pip3 install tinydb
RUN pip3 install flask
RUN pip3 install requests

WORKDIR ${SCRIPT_ROOT}

ADD crawler/crawler.py crawler.py

ENTRYPOINT ["python", "-u", "crawler.py"]