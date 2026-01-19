# frontend/Dockerfile
FROM nginx:alpine

# Remove default nginx static content
RUN rm -rf /usr/share/nginx/html/*

# Copy our static frontend
COPY frontend/index.html /usr/share/nginx/html/index.html
COPY frontend/main.js /usr/share/nginx/html/main.js

# Expose Nginx port
EXPOSE 80

# Default command is already `nginx -g "daemon off;"`
