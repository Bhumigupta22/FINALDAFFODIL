FROM node:18-alpine as builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM python:3.11-slim

WORKDIR /app

# Serve static files with simple HTTP server
RUN pip install http-server

# Copy built frontend
COPY --from=builder /app/dist /app/dist

EXPOSE 3000

CMD ["python", "-m", "http.server", "3000", "--directory", "/app/dist"]
