FROM node:lts-alpine
COPY . .
RUN npm ci
RUN npm run build
CMD [ "node", "dist/main.js"]
