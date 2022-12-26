FROM python:3.8-ubi8

RUN pip3 install fastapi

WORKDIR /usr/src/app
ADD . .
RUN pip install -r requirements.txt

EXPOSE 8080
CMD uvicorn simple-fastapi:app --host 0.0.0.0 --port 8080
