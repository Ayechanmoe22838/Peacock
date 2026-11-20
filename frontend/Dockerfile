# Production Nginx reverse-proxy and static asset server for PEACOCK Frontend
FROM nginx:alpine

# Remove default nginx configurations
RUN rm -f /etc/nginx/conf.d/default.conf

# Copy Nginx template for runtime PORT and BACKEND_URL variable substitution
COPY frontend/nginx.conf.template /etc/nginx/templates/default.conf.template
COPY frontend/nginx.conf /etc/nginx/nginx.conf

# Copy static assets and media files from the application
COPY app/static /usr/share/nginx/html/static
COPY media /usr/share/nginx/html/media

# Copy frontend entrypoint script
COPY frontend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Default environment variables for Railway and Docker
ENV PORT=80
ENV BACKEND_URL=http://backend:8000

EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://localhost:${PORT}/health || exit 1

ENTRYPOINT ["/entrypoint.sh"]
