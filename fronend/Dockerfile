# FROM tiangolo/node-frontend:10 as build-stage
# WORKDIR /app
# COPY package*.json /app/
# RUN npm install
# COPY ./ /app/
# RUN npm run build

# FROM nginx:1.15
# COPY --from=build-stage /app/build/ /usr/share/nginx/html
# COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Install dependencies
FROM node:alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

CMD ["yarn", "start"]