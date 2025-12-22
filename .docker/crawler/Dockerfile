FROM python:3

RUN apt-get update
RUN pip3 install tinydb
RUN pip3 install flask
RUN pip3 install requests
RUN pip3 install python-crontab
RUN apt-get update && apt-get -y install cron

ENV SCRIPT_ROOT=/var/www
#ENV DB_PATH=/data/sites.json
#ENV cron="0 12 * * *"
#ENV database="sites.json"

WORKDIR ${SCRIPT_ROOT}

ADD crawler/crawler.py crawler.py
ADD --chmod=777 crawler/cron-install.sh cron-install.sh
ADD --chmod=777 crawler/run.sh run.sh

# Run the command on container startup
# Any start arguments will be appended after the cronjob string
ENTRYPOINT ["./run.sh"]