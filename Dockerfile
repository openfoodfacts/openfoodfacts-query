FROM node:lts-alpine
COPY ./src ./src
COPY ./package* .
COPY ./tsconfig.* .
RUN npm ci
RUN npm run build
CMD [ "node", "dist/main.js"]
