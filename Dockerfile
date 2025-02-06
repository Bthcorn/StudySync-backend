FROM python:3.11-slim

RUN apt update && apt install -y \
    libpq-dev \
    && pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
