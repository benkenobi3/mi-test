FROM python:alpine

WORKDIR /app

COPY ./requirements.txt /app

RUN apk update && \
    apk add --no-cache --virtual build-deps gcc make python3-dev musl-dev jpeg-dev zlib-dev libffi-dev openssl-dev&& \
    pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && \
    apk del build-deps

COPY ./ /app

ENTRYPOINT ["python", "src/app.py"]