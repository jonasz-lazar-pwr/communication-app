# Bazowy obraz
FROM node:18-alpine

# Ustaw katalog roboczy
WORKDIR /app

# Kopiowanie plików zależności
COPY package.json package-lock.json ./

# Instalacja zależności i czyszczenie cache npm
RUN npm install && npm cache clean --force

# Kopiowanie całego projektu
COPY . .

# Eksponowanie portu Angulara
EXPOSE 4200

# Komenda startowa w trybie deweloperskim
CMD ["npm", "start"]


## Etap budowania aplikacji
#FROM node:18-alpine AS build-stage
#
## Ustaw katalog roboczy
#WORKDIR /app
#
## Kopiowanie plików zależności
#COPY package.json package-lock.json ./
#
## Instalacja zależności
#RUN npm install
#
## Kopiowanie całego projektu (z wyjątkiem ignorowanych w .dockerignore)
#COPY . .
#
## Budowanie aplikacji Angular
#RUN npm run build -- --output-path=dist --configuration development
#
## Etap produkcyjny (lub rozwój, w zależności od wymagań)
#FROM node:18-alpine
#
## Ustaw katalog roboczy
#WORKDIR /app
#
## Kopiowanie zbudowanej aplikacji z poprzedniego etapu
#COPY --from=build-stage /app/dist /app/dist
#
## Instalacja minimalnej liczby narzędzi potrzebnych do uruchomienia
#COPY package.json package-lock.json ./
#RUN npm install --omit=dev
#
## Eksponowanie portu dla Angular CLI (lub serwera w trybie produkcji)
#EXPOSE 4200
#
## Komenda startowa w trybie deweloperskim
#CMD ["npx", "http-server", "/app/dist", "-p", "4200"]
