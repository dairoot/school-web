FROM python:3.6.5

MAINTAINER dairoot

WORKDIR /home

RUN echo 'Asia/Shanghai' > /etc/timezone && /bin/ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

ADD . /home

RUN pip install -U pip && pip install -r requirements.txt
