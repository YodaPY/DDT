FROM python:3.9

COPY ./requirements.txt /bot/requirements.txt

WORKDIR /bot

RUN apt update && apt install -y libmagic1

RUN pip install -Ur requirements.txt

COPY . /bot

ENTRYPOINT python -OO -m dtv
