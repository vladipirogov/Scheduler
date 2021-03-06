FROM python:3-slim

SHELL ["/bin/bash", "-c"]

RUN useradd -m user

WORKDIR /home/user

RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip3 install psycopg2~=2.6

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN source venv/bin/activate
RUN pip install -r requirements.txt
RUN pip install -U eventlet
RUN pip install gunicorn

COPY app app
COPY migrations migrations
COPY runner.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP owl.py

RUN chown -R user:user ./
USER user

EXPOSE 5000
ENTRYPOINT ["sh","./boot.sh"]

#docker build -t flask-home:latest .
#docker run --name home -d -p 5000:5000 -e TZ=Europe/Kiev flask-home:latest