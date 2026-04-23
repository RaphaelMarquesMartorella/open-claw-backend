FROM ghcr.io/puppeteer/puppeteer:22.12.1

ENV NODE_ENV=production \
    PUPPETEER_SKIP_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome

WORKDIR /app

USER root

COPY package.json ./
RUN npm install --omit=dev

COPY index.js ./

RUN chown -R pptruser:pptruser /app

USER pptruser

EXPOSE 3001

CMD ["node", "index.js"]
