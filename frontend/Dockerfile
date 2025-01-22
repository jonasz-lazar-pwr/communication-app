# Bazowy obraz
FROM node:18

# Ustaw katalog roboczy
WORKDIR /app

# Kopiowanie plików projektu
COPY package.json package-lock.json /app/

# Instalacja zależności Node.js
RUN npm install

# Kopiowanie całej aplikacji
COPY . /app/

# Port dla Angulara
EXPOSE 4200

# Komenda startowa
CMD ["npm", "start"]