FROM python:3.7.3-stretch

RUN mkdir -p /home/app
RUN adduser app
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY app.py .
COPY requirements.txt .

# hadolint ignore=DL3013
RUN pip3 install --upgrade pip &&\
    pip3 install -r requirements.txt

EXPOSE 8080

RUN chown -R app:app $APP_HOME
USER app

ENTRYPOINT ["gunicorn", "-b", ":8080", "app:app"]