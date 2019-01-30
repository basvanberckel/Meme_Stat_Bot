FROM python:3.6-alpine

COPY  . /

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]