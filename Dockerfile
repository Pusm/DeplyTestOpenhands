# Multi-stage build for production
FROM node:18-alpine as builder

# Build frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN npm run build

# Build backend
WORKDIR /app/backend
COPY backend/package*.json ./
RUN npm install
COPY backend .

# Production image
FROM node:18-alpine
WORKDIR /app

# Copy built frontend
COPY --from=builder /app/frontend/dist ./frontend/dist

# Copy backend
COPY --from=builder /app/backend ./backend

# Install production dependencies
WORKDIR /app/backend
RUN npm install --production

# Install serve for frontend
RUN npm install -g serve

# Expose ports
EXPOSE 54935 59175

# Start both services
CMD (cd /app/backend && node index.js &) && serve -s /app/frontend/dist -l 59175