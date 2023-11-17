FROM python:3.10.12-slim
 
WORKDIR /app/live-now-job

RUN apt-get update && apt-get -y install cron

# ADD ./requirements.txt /app/live-now-job/requirements.txt
COPY . /app/live-now-job
COPY crontab /etc/cron.d/crontab

# RUN pip install -r requirements.txt



RUN chmod 0644 /etc/cron.d/crontab
RUN mkdir /var/log/cron
# RUN touch /var/log/cron/cron.log
# -f  ：強制進行，而不去判斷時間記錄檔的時間戳記；
CMD ["cron", "-f"]