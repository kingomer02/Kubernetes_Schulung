FROM python:3.9-alpine

WORKDIR /app

COPY . .

RUN pip install flask requests

ENV FE_PORT=8080

EXPOSE 80

CMD ["python", "frontend.py"]