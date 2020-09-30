FROM python:3.8-alpine
MAINTAINER HPS Cloud Services

# https://stackoverflow.com/questions/46221063/what-is-build-deps-for-apk-add-virtual-command
# https://www.sandtable.com/reduce-docker-image-sizes-using-alpine/
# https://stackoverflow.com/questions/37015624/how-to-run-a-cron-job-inside-a-docker-container
# https://blog.knoldus.com/running-a-cron-job-in-docker-container/
# https://stackoverflow.com/questions/37458287/how-to-run-a-cron-job-inside-a-docker-container
# https://jonathas.com/scheduling-tasks-with-cron-on-docker/
# https://medium.com/@ievstrygul/using-cron-inside-a-docker-container-to-execute-jar-3599b2a398cb
# https://medium.com/@ievstrygul/wiring-scala-app-docker-container-with-mongodb-84b29c50ac5

# aiohttp installtion throws installation exception, have to fix that if we are using

WORKDIR /app
COPY . .
#RUN echo "PWD";cd $PWD;ls -ltr

ARG DOCKER_HOST_IP
ENV DOCKER_HOST_IP=$DOCKER_HOST_IP

RUN set -ex \
    apk update && apk upgrade -f \
    && apk add --no-cache \
    curl \
    bash \
    && pip3 install --upgrade pip setuptools wheel \
    && pip3 install --no-cache -r requirements.txt && \
    chmod 744 ./http_request_executor.py ./component_health_check.py ./entrypoint.sh && \
    /usr/bin/crontab ./crontab.txt

CMD ["./entrypoint.sh"]