FROM python:3.10-alpine
MAINTAINER alexandr
RUN apk add --upgrade tzdata
RUN python3 -m pip install --upgrade pip
COPY . /bot_asus
WORKDIR /bot_asus
RUN python3 -m pip install -r requirements.txt
ENV TZ=Europe/Moscow
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
CMD ["python3", "bot.py"]

