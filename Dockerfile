FROM python:3.9.16-slim

COPY ./app /app
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8082

CMD ["python3", "app.py"]