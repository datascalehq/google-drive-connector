FROM python:3.8

ADD /app /root/app
ADD /requirements.txt /root/requirements.txt
ADD /Makefile /root/Makefile
ADD /credentials /root/credentials

WORKDIR /root
RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD make api_start