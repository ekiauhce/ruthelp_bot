FROM python:3.8.5-slim

ENV TG_API_TOKEN=TOKEN

RUN python3 -m pip install --upgrade pip
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY src/ /tmp/src/
WORKDIR /tmp/src/

RUN python3 init_db.py

ENTRYPOINT ["python3", "main.py"]