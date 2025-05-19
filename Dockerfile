# Simple production image
FROM nginx:alpine

# Copy frontend files
COPY frontend /usr/share/nginx/html

# Copy backend
COPY backend /app/backend

# Expose ports
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]