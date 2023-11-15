FROM python:3.10.12-slim
 
WORKDIR /app/live-now-job

ADD ./requirements.txt /app/live-now-job/requirements.txt

RUN pip install -r requirements.txt

ADD . /app/live-now-job

CMD python3 chat_gpt_test.py