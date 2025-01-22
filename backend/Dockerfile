# Bazowy obraz
FROM python:3.11-slim

# Ustawienia środowiska
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Ustaw katalog roboczy
WORKDIR /app

# Instalacja zależności Pythona
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie aplikacji
COPY . /app/

# Port dla serwera Django
EXPOSE 8000

# Komenda startowa
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]