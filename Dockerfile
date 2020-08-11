FROM python:3.8-alpine

MAINTAINER Timur Samkharadze "timur.samkharadze@gmail.com"

COPY ./* /service/
WORKDIR /service

RUN pip install -r requirements.txt

EXPOSE 5000/tcp

ENTRYPOINT ["python3"]
CMD ["service.py"]