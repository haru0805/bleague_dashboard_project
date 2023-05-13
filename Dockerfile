FROM python:3.9
USER root

RUN apt update
RUN apt -y install locales
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install selenium beautifulsoup4
RUN pip install requests
RUN pip install pandas
COPY ./app/source/test.py /root/source/