FROM python:3.12-slim

# disable .pyc files + output buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# install dependencies
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip \
 && pip install -r /tmp/requirements.txt

# default command (will be overridden by compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]