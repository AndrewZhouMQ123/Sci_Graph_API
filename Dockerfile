FROM python:3.13.1-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  gfortran \
  libatlas-base-dev \
  libopenblas-dev \
  liblapack-dev \
  libffi-dev \
  libpng-dev \
  libfreetype6-dev \
  && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --no-compile --prefix=/install -r requirements.txt
COPY . .
FROM python:3.13.1-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
  libatlas-base-dev \
  libopenblas-dev \
  liblapack-dev \
  libfreetype6 \
  libpng-dev \
  && rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /usr/local
COPY --from=builder /app /app
EXPOSE 8080
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8080", "--log-level=debug"]