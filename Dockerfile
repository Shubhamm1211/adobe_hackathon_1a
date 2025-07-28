FROM --platform=linux/amd64 python:3.11-alpine AS builder

WORKDIR /app

RUN apk add --no-cache make gcc g++ musl-dev binutils

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN find /usr/local/lib/python3.11/site-packages -name "*.so" -exec strip {} +


FROM --platform=linux/amd64 python:3.11-alpine

WORKDIR /app

COPY main.py .

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

CMD ["python", "main.py"]