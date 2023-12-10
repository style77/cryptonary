FROM python:3.11

RUN apt-get update && apt-get install -y cron

COPY job.sh /root/job.sh
RUN chmod +x /root/job.sh

COPY crontab /etc/cron.d/cron-job
RUN chmod 0644 /etc/cron.d/cron-job
RUN crontab /etc/cron.d/cron-job

CMD ["cron", "-f"]