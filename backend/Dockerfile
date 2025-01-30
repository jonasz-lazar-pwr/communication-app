# Etap budowania zależności
FROM python:3.11-alpine AS build-stage

# Ustawienia środowiska
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalacja narzędzi i zależności wymaganych do budowania
RUN apk add --no-cache gcc musl-dev libpq-dev

# Ustaw katalog roboczy
WORKDIR /app

# Kopiowanie pliku z zależnościami
COPY requirements.txt ./

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Etap finalny
FROM python:3.11-alpine

# Ustawienia środowiska
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ustaw katalog roboczy
WORKDIR /app

# Kopiowanie zależności z etapu budowania
COPY --from=build-stage /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build-stage /usr/local/bin /usr/local/bin

# Kopiowanie kodu aplikacji
COPY . .

# Otwórz port dla aplikacji
EXPOSE 8000

# Usuń tymczasowe pliki i cache (opcjonalne, na wypadek dodatkowych buildów)
RUN rm -rf /root/.cache

# Komenda startowa
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver_plus 0.0.0.0:8000"]