FROM  ubuntu:20.04
FROM  python:3.12

ENV PATH="/scripts:${PATH}"

# Always flush output directly
ENV PYTHONBUFFERED=1

# Install Java
RUN apt-get update && \
    apt install -y default-jdk && \
    apt-get clean;

# install dependencies
COPY ./requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

# add the code to the docker image
RUN mkdir /app
COPY ./src /app
WORKDIR /app
COPY ./scripts /scripts

# add executable permission to the scripts folder
# scripts will run a uwsgi service that will host the app
RUN chmod +x /scripts/*

# add directories for static
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# create a new user in the docker image to run the server, not as root
RUN adduser user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web

RUN chmod -R 755 /app/logs
RUN chmod -R 666 /app/transmission/processing/temp
RUN chmod -R 666 /app/home/temp
RUN chmod -R 666 /app/de421.bsp
# switch to unprivileged user
USER user

# run the startup script
CMD ["entrypoint.sh"]
