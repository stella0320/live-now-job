FROM python:3.10.12-slim
 
WORKDIR /app/live-now-job

RUN apt-get update && apt-get -y install cron

# ADD ./requirements.txt /app/live-now-job/requirements.txt

COPY crontab /etc/cron.d/crontab

# RUN pip install -r requirements.txt

ADD . /app/live-now-job

RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

# CMD python3 indievoxCrawlerJob.py
CMD ["cron", "-f", "-d", "8"]