FROM python:3

EXPOSE 5000/tcp

HEALTHCHECK --interval=1m --timeout=5s --retries=3 --start-period=20s --start-interval=1s \
  CMD curl -f http://localhost:5000/health || exit 1

ENV SCRIPT_ROOT=/var/www
#ENV FLASK_APP=${SCRIPT_ROOT}/server/server.py

WORKDIR ${SCRIPT_ROOT}

ADD server/server.py .
ADD server/requirements.txt .
ADD server/templates/ ./templates/
ADD server/static/ ./static/

RUN apt-get update
RUN pip3 install -r requirements.txt
RUN apt-get -y upgrade

ENTRYPOINT ["python", "-u", "server.py"]
#args passed directly to entrypoint