FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip
COPY --chown=1001:0 ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY src/ /app/src/

CMD ["python", "src/main.py", "-l", "20"]
