FROM python:3.10.12-slim
 
WORKDIR /app/live-now-job

RUN apt-get update && apt-get -y install cron

# ADD ./requirements.txt /app/live-now-job/requirements.txt
COPY . /app/live-now-job
COPY crontab /etc/cron.d/hello-crontab

# RUN pip install -r requirements.txt



RUN chmod 0644 /etc/cron.d/hello-crontab

RUN touch /var/log/cron.log



# CMD python3 indievoxCrawlerJob.py
CMD cron && tail -f /var/log/cron.log