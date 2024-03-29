FROM python:3.11

WORKDIR /app

COPY src/ /app/src/

COPY --chown=1001:0 ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
CMD ["python", "src/main.py", "-l", "20"]
