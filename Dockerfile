FROM python:3.6.5

MAINTAINER dairoot

WORKDIR /home

RUN echo 'Asia/Shanghai' > /etc/timezone && /bin/ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

ADD requirements.txt .

RUN pip install -U pip && pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com 

ADD . /home
