FROM python:3.9-alpine
WORKDIR /app
COPY . .
RUN pip install flask 

ENV BE_PORT=8081

EXPOSE 80
CMD ["python", "backend.py"]
