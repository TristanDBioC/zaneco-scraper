FROM python:3.12
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["sh", "-c", "while :; do python main.py; sleep 3600; done"]
