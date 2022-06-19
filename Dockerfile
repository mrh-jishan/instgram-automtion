FROM ubuntu:latest

WORKDIR /app

# Add the script to the Docker Image
ADD . /app

# Give execution rights on the cron scripts
RUN chmod -R 0644 /app

RUN apt-get update

RUN apt-get install -y python3 python3-pip

RUN pip install -r requirements.txt

#Install Cron
RUN apt-get -y install cron

ADD crontab /etc/cron.d/

# Run the command on container startup
CMD cron