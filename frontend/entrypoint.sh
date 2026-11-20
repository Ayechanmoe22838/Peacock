#!/bin/sh
set -e

echo "=========================================================="
echo "🦚 PEACOCK WEDDING SYSTEM – FRONTEND (NGINX) GATEWAY"
echo "=========================================================="

PORT="${PORT:-80}"
BACKEND_URL="${BACKEND_URL:-http://backend:8000}"

echo "📍 Nginx listening on port: ${PORT}"
echo "🔗 Upstream backend target: ${BACKEND_URL}"

# Substitute environment variables in Nginx configuration template
envsubst '${PORT} ${BACKEND_URL}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Test Nginx configuration syntax
nginx -t

echo "🚀 Starting Nginx..."
exec nginx -g 'daemon off;'
