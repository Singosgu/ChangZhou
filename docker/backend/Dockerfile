FROM python:3.9-slim as base
RUN mkdir -p /GreaterWMS/templates
#copy requirements.txt
ADD ./requirements.txt /GreaterWMS/requirements.txt 
#Configure working directory
WORKDIR /GreaterWMS
#Installation foundation dependency
RUN sed -i s/deb.debian.org/mirrors.163.com/g /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update --fix-missing && apt-get upgrade -y
RUN apt-get install build-essential -y
RUN apt-get install supervisor -y
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN apt-get install build-essential -y
RUN apt-get install supervisor -y
RUN python3 -m pip install --upgrade pip
#Install supervisor
RUN pip3 install supervisor
RUN pip3 install -U 'Twisted[tls,http2]'
RUN pip3 install setuptools
RUN pip3 install eventlet
RUN pip3 install greenlet
RUN pip3 install pandas
RUN pip3 install SQLAlchemy
RUN pip3 install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
EXPOSE 8008
