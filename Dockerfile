FROM python:3.9.16-slim

WORKDIR /app/live-now-job

COPY . /app/live-now-job

RUN apt-get update && apt-get -y install cron vim
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



# modify the permission on crontab file
COPY ./crontab /etc/cron.d/crontab

RUN chmod 0644 /etc/cron.d/crontab 
RUN /usr/bin/crontab /etc/cron.d/crontab


RUN chmod 0644 /app/live-now-job


RUN mkdir -p /var/log/cron
RUN chmod 0644 /var/log/cron
# RUN touch /var/log/cron/cron.log
# RUN /var/log/cron-2023-11-17.log

VOLUME /var/log/cron

# -f  ：強制進行，而不去判斷時間記錄檔的時間戳記；
CMD ["cron","-f", "-l", "2"]
