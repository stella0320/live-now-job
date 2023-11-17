FROM python:3.10.12-slim
 
WORKDIR /app/live-now-job

RUN apt-get update && apt-get -y install cron vim

# ADD ./requirements.txt /app/live-now-job/requirements.txt
COPY . /app/live-now-job
RUN chmod 0644 /app/live-now-job/hello.py
ADD crontab /etc/cron.d/crontab

# RUN pip install -r requirements.txt



RUN chmod 0644 /etc/cron.d/crontab
# RUN mkdir -p /var/log/cron
# RUN chmod 0644 /var/log/cron
RUN touch /var/log/cron-2023-11-17.log
# -f  ：強制進行，而不去判斷時間記錄檔的時間戳記；
CMD /usr/sbin/cron -f 