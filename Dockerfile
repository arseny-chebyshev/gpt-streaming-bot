FROM python:3.10.11-slim-buster as root

WORKDIR /bot/
COPY requirements.txt /bot/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

FROM python:3.10.11-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /bot/
COPY --from=root /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=root /usr/local/bin/ /usr/local/bin/
COPY . /bot/
