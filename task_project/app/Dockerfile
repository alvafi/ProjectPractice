FROM python:3.10-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8888

CMD ["python", "App.py", "--ip", "0.0.0.0", "--port", "8080", "--no-browser"]