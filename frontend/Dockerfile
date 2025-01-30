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

# Start the application in development mode
CMD ["npm", "start", "--", "--host=0.0.0.0", "--ssl=true", "--ssl-cert=certs/localhost-cert.pem", "--ssl-key=certs/localhost-key.pem"]