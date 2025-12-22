FROM python:3

EXPOSE 5000/tcp

ENV SCRIPT_ROOT=/var/www
#ENV FLASK_APP=${SCRIPT_ROOT}/server/server.py

RUN apt-get update
RUN pip3 install tinydb
RUN pip3 install flask

WORKDIR ${SCRIPT_ROOT}

ADD server/server.py .
ADD server/templates/ ./templates/
ADD server/static/ ./static/

ENTRYPOINT ["python", "-u", "server.py"]
#args passed directly to entrypoint