FROM ubuntu:latest

WORKDIR /app

# Add the script to the Docker Image
ADD . /app

# Give execution rights on the cron scripts
RUN chmod -R 0644 /app

RUN apt-get update

RUN apt-get install -y python3 python3-pip

RUN apt-get install -y vim

RUN pip install -r requirements.txt

#Install Cron
RUN apt-get -y install cron

# ADD crontab /etc/cron.d/

# # Run the command on container startup
# CMD crontab

# Copy hello-cron file to the cron.d directory
COPY crontab /etc/cron.d/insta-cron
 
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/insta-cron

# Apply cron job
RUN crontab /etc/cron.d/insta-cron
 
# Create the log file to be able to run tail
RUN touch /var/log/insta.log
 
# Run the command on container startup
CMD cron && tail -f /var/log/insta.log