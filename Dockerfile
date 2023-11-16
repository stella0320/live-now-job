FROM python:3.10.12-slim
 
WORKDIR /app/live-now-job

RUN apt-get update && apt-get install -y cron && cron

# ADD ./requirements.txt /app/live-now-job/requirements.txt
COPY . /app/live-now-job
COPY crontab /etc/cron.d/crontab

# RUN pip install -r requirements.txt



RUN chmod +x hello.py
RUN crontab /etc/cron.d/crontab

# CMD python3 indievoxCrawlerJob.py
CMD ["cron", "-f"]