FROM python:3


ENV SCRIPT_ROOT=/var/www
#ENV DB_PATH=/data/sites.json
#ENV cron="0 12 * * *"
#ENV database="sites.json"

WORKDIR ${SCRIPT_ROOT}

ADD crawler/crawler.py .
ADD crawler/requirements.txt .
ADD --chmod=777 crawler/cron-install.sh cron-install.sh
ADD --chmod=777 crawler/run.sh run.sh

RUN apt-get update
RUN pip3 install -r requirements.txt
RUN apt-get -y upgrade && apt-get -y install cron

# Run the command on container startup
# Any start arguments will be appended after the cronjob string
ENTRYPOINT ["./run.sh"]