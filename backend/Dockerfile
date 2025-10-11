FROM python:3.12-slim

# disable .pyc files + output buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# install dependencies first for better caching
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip \
 && pip install -r /tmp/requirements.txt

# copy project files
COPY . .

EXPOSE 8000

# default command (will be overridden by compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]