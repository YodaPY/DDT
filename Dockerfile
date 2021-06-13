FROM python:3.9

COPY ./requirements.txt /bot/requirements.txt

WORKDIR /bot

RUN pip install -Ur requirements.txt

COPY . /bot

ENTRYPOINT python -OO -m dtv