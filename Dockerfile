FROM python:3.14-slim
WORKDIR /app
COPY . .
EXPOSE 8080
CMD ["python", "api/server.py"]
