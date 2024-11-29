# Dockerfile (base service template - create one for each service)
FROM python:3.11-slim

WORKDIR /app


RUN apt-get update && apt-get install -y default-mysql-client && apt-get clean && rm -rf /var/lib/apt/lists/* && apt-get clean
# COPY shared /app/shared
COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -U -r requirements.txt && rm -rf /root/.cache/pip

# Install specific packages mentioned in the error
RUN pip install fastapi uvicorn
# RUN pip install -e .

COPY . /app/

# Changed from "app.main:app" to "main:app" to match your structure
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8006", "--reload"]