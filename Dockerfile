FROM python:3.8.7-buster

WORKDIR /service

RUN addgroup app_user && adduser --ingroup app_user app_user && chown -R app_user:app_user /service

COPY --chown=app_user requirements.txt /service/requirements.txt
COPY --chown=app_user app.py /service/app.py
COPY --chown=app_user templates /service/templates

RUN pip3 install -r requirements.txt --no-cache-dir

USER app_user

CMD [ "flask", "run", "--host", "0.0.0.0"]
