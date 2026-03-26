FROM python:3

EXPOSE 5000/tcp

ENV SCRIPT_ROOT=/var/www
#ENV FLASK_APP=${SCRIPT_ROOT}/server/server.py
#ENV DB_PATH=/data/sites.json
#ENV cron="0 12 * * *"
#ENV database="sites.json"

WORKDIR ${SCRIPT_ROOT}

RUN mkdir server crawler

ADD --chmod=777 .docker/combined/combined-startup.sh .

ADD server/ ./server/

ADD crawler/ ./crawler/
ADD  crawler/cron-install.sh ./crawler/cron-install.sh
ADD --chmod=777 crawler/run.sh ./crawler/run.sh

RUN apt-get update -y
RUN pip3 install -r server/requirements.txt && pip3 install -r crawler/requirements.txt
RUN apt-get -y upgrade && apt-get -y install cron

# Run the command on container startup
ENTRYPOINT ["./combined-startup.sh"]
