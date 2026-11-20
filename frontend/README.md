# Frontend Architecture & Deployment – PEACOCK

This folder contains the Docker, Nginx, and Railway configuration for the **PEACOCK** frontend gateway service.

---

## 🎨 Overview

The frontend architecture consists of:
1. **Server-Side Rendered Jinja2 Templates**:
   - `app/templates/public/`: Public wedding showcase, venue catalog, interactive RSVP studio.
   - `app/templates/customer/`: Customer portal, budget tracker, seating planner, catering menus.
   - `app/templates/admin/`: Administrator dashboards, booking management, financial audit queue.
2. **Design System & Static Assets**:
   - `app/static/css/peacock.css`: Official 11 Peacock colors, Light Mode (Black `#000000` text) and Dark Mode (White `#ffffff` text).
   - `app/static/js/peacock.js`: Instant dual-theme switching with localStorage persistence, Chart.js dynamic color synchronizer.
   - `app/static/images/`: 13 stationery invitation templates, 12 Myanmar & International food dishes, 8 venue halls, receipt samples.
3. **High-Performance Nginx Gateway**:
   - Serves static CSS, JS, and images with `Cache-Control: public, max-age=604800, immutable` and gzip compression.
   - Serves uploaded media with client caching.
   - Reverse proxies dynamic HTML rendering and API traffic to the FastAPI backend.
   - Configurable upstream via `BACKEND_URL`.

---

## 🐳 Docker Deployment

### Building the Image Locally
```bash
docker build -t peacock-frontend -f frontend/Dockerfile .
```

### Running the Container
```bash
docker run -p 80:80 \
  -e PORT=80 \
  -e BACKEND_URL=http://host.docker.internal:8000 \
  peacock-frontend
```

---

## 🚂 Railway Deployment

When deploying the frontend as a microservice on Railway:

1. **Create a New Service** connected to your repository.
2. In **Settings**:
   - Set **Dockerfile Path** to `frontend/Dockerfile`.
3. In **Variables**:
   - Set `BACKEND_URL`: The private networking domain of your backend service (e.g. `http://${{peacock-backend.RAILWAY_PRIVATE_DOMAIN}}:8000`) or public backend URL.
4. Railway will automatically assign a `$PORT` and generate a public HTTPS domain.
