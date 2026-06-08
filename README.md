# 🚗 Campus Ride — Distributed Systems Project (STIJK2124)

> A campus-based ride-sharing application built on a 3-tier distributed architecture using FastAPI, Next.js, PostgreSQL, and Kubernetes. Deployed on Railway with Supabase authentication.

---

## 📐 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT TIER (Tier 1)                         │
│                                                                     │
│   ┌──────────────────────────────────────────────────────────┐      │
│   │           Next.js Frontend (React + Tailwind)            │      │
│   │         Deployed on Railway  |  Port 3000 (local)        │      │
│   └────────────────────────┬─────────────────────────────────┘      │
└────────────────────────────│────────────────────────────────────────┘
                             │  HTTP/HTTPS REST API calls
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     APPLICATION TIER (Tier 2)                       │
│                                                                     │
│   ┌──────────────────────────────────────────────────────────┐      │
│   │              FastAPI Backend (Python)                     │      │
│   │         Deployed on Railway  |  Port 8000 (local)        │      │
│   │                                                          │      │
│   │   /auth/*        /rides/*        /users/*               │      │
│   │   (Supabase)     (Booking)       (Profile)              │      │
│   └────────────────────────┬─────────────────────────────────┘      │
└────────────────────────────│────────────────────────────────────────┘
                             │  SQL queries via asyncpg / SQLAlchemy
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       DATA TIER (Tier 3)                            │
│                                                                     │
│   ┌──────────────────────────────────────────────────────────┐      │
│   │         PostgreSQL Database (Supabase-hosted)            │      │
│   │              Port 5432  |  SSL enforced                  │      │
│   │                                                          │      │
│   │   Tables: users, rides, bookings, locations             │      │
│   └──────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                     INFRASTRUCTURE LAYER                            │
│                                                                     │
│   Docker Compose (local dev)    Kubernetes (k8s) manifests          │
│   ├── backend service           ├── backend.yaml                    │
│   ├── frontend service          ├── frontend.yaml                   │
│   └── postgres service          ├── postgres.yaml                   │
│                                 ├── configmap.yaml                  │
│   Railway (cloud deployment)    ├── secret.yaml                     │
│   ├── backend service           ├── ingress.yaml                    │
│   └── frontend service          └── hpa.yaml                        │
│                                                                     │
│   Authentication: Supabase Auth (JWT-based)                         │
│   Load Testing:   Artillery                                          │
│   Monitoring:     Wireshark (network capture)                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ✅ Prerequisites

| Tool | Version | Purpose | Installation |
|------|---------|---------|--------------|
| Node.js | ≥ 18.x | Run Next.js frontend | [nodejs.org](https://nodejs.org) |
| pnpm | ≥ 8.x | Package manager (frontend) | `npm i -g pnpm` |
| Python | ≥ 3.11 | Run FastAPI backend | [python.org](https://python.org) |
| pip | ≥ 23.x | Python package manager | Bundled with Python |
| Docker | ≥ 24.x | Containerization | [docs.docker.com](https://docs.docker.com/get-docker/) |
| Docker Compose | ≥ 2.x | Multi-container orchestration | Bundled with Docker Desktop |
| kubectl | ≥ 1.28 | Kubernetes CLI | [kubernetes.io](https://kubernetes.io/docs/tasks/tools/) |
| Minikube | ≥ 1.32 | Local Kubernetes cluster | [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/docs/start/) |
| Wireshark | ≥ 4.x | Network packet capture | [wireshark.org](https://www.wireshark.org/download.html) |
| Artillery | ≥ 2.x | Load testing | `npm i -g artillery` |
| Git | ≥ 2.x | Version control | [git-scm.com](https://git-scm.com) |
| Supabase account | — | Auth + hosted PostgreSQL | [supabase.com](https://supabase.com) |
| Railway account | — | Cloud deployment | [railway.app](https://railway.app) |

---

## 🚀 Setup Instructions (Parts 1–7)

### Part 1 — Project Initialization & Repository Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/dist-sys-app.git
   cd dist-sys-app
   ```

2. **Set up Supabase project:**
   - Go to [supabase.com](https://supabase.com) → New Project
   - Run the migration file to initialize the database schema:
     ```bash
     # In Supabase SQL Editor, paste contents of:
     supabase/migrations/001_university_ride.sql
     ```
   - Copy your **Project URL**, **Anon Key**, and **Service Role Key** from *Settings → API*

3. **Configure environment variables** (see [Environment Variables](#-environment-variables) section below)

---

### Part 2 — Backend Setup (FastAPI)

1. **Navigate to the backend service directory:**
   ```bash
   cd services/backend   # adjust path as needed
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend locally:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. **Verify:** Visit `http://localhost:8000/docs` — you should see the FastAPI Swagger UI.

---

### Part 3 — Frontend Setup (Next.js)

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   pnpm install
   ```

3. **Create `.env.local`:**
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

4. **Run the frontend:**
   ```bash
   pnpm dev
   ```

5. **Verify:** Open `http://localhost:3000`

---

### Part 4 — Docker Compose (Local Containerized Run)

1. **Ensure Docker Desktop is running**

2. **From the project root, build and start all services:**
   ```bash
   docker-compose up --build
   ```

3. **Services will be available at:**
   | Service | URL |
   |---------|-----|
   | Frontend | http://localhost:3000 |
   | Backend API | http://localhost:8000 |
   | PostgreSQL | localhost:5432 |

4. **To stop:**
   ```bash
   docker-compose down
   ```

---

### Part 5 — Kubernetes Deployment (Minikube)

1. **Start Minikube:**
   ```bash
   minikube start
   ```

2. **Apply ConfigMap and Secrets first:**
   ```bash
   kubectl apply -f k8s/configmap.yaml
   kubectl apply -f k8s/secret.yaml
   ```

3. **Apply all workload manifests:**
   ```bash
   kubectl apply -f k8s/postgres.yaml
   kubectl apply -f k8s/backend.yaml
   kubectl apply -f k8s/frontend.yaml
   kubectl apply -f k8s/ingress.yaml
   kubectl apply -f k8s/hpa.yaml
   ```

4. **Check pod status:**
   ```bash
   kubectl get pods
   kubectl get services
   ```

5. **Access the app via Minikube:**
   ```bash
   minikube service frontend-service --url
   ```

---

### Part 6 — Wireshark Network Capture

1. **Open Wireshark** and select your active network interface (e.g., Wi-Fi or Ethernet)

2. **Apply capture filters** (see [Wireshark Filter Reference](#-wireshark-filter-reference) below)

3. **Perform actions in the app** (login, book a ride, etc.) while Wireshark is capturing

4. **Stop the capture** and save as `.pcapng`

5. **Apply display filters** to isolate relevant traffic and take screenshots for your report

> See the [Wireshark Filter Reference](#-wireshark-filter-reference) section for specific filters used.

---

### Part 7 — Artillery Load Testing

1. **Ensure the backend is running** (either locally or deployed on Railway)

2. **Run the load test:**
   ```bash
   artillery run load-test.yml
   ```

3. **Generate an HTML report:**
   ```bash
   artillery run load-test.yml --output result.json
   artillery report result.json
   ```

4. **The `load-test.yml` configuration targets:**
   - Endpoint: your Railway backend URL
   - Phases: warm-up (10 users/sec for 30s) → ramp-up (50 users/sec for 60s)
   - Scenarios: GET `/rides`, POST `/auth/login`, GET `/users/me`

5. **Save screenshots of:**
   - Terminal output showing requests/sec and latency
   - The generated HTML report graphs

---

## 🔐 Environment Variables

### Backend (`services/backend/.env`)

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `DATABASE_URL` | Full PostgreSQL connection string | Supabase → Settings → Database → Connection String |
| `SUPABASE_URL` | Your Supabase project URL | Supabase → Settings → API → Project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Admin key for server-side auth operations | Supabase → Settings → API → Service Role Key |
| `SUPABASE_ANON_KEY` | Public key for client-side operations | Supabase → Settings → API → Anon/Public Key |
| `SECRET_KEY` | JWT signing secret for session tokens | Generate: `openssl rand -hex 32` |
| `ALGORITHM` | JWT algorithm (default: `HS256`) | Set manually |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry duration in minutes | Set manually (e.g., `30`) |

### Frontend (`frontend/.env.local`)

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `NEXT_PUBLIC_API_URL` | Backend base URL | Railway backend deployment URL |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | Supabase → Settings → API |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase public anon key | Supabase → Settings → API |

> ⚠️ **Never commit `.env` files to Git.** They are listed in `.gitignore`.

---

## ☸️ Kubernetes Manifest Files

| File | Kind | Description |
|------|------|-------------|
| `k8s/backend.yaml` | Deployment + Service | Deploys the FastAPI backend with 2 replicas; exposes port 8000 via ClusterIP |
| `k8s/frontend.yaml` | Deployment + Service | Deploys the Next.js frontend with 1 replica; exposes port 3000 via NodePort |
| `k8s/postgres.yaml` | StatefulSet + Service | Deploys PostgreSQL with persistent volume claim; exposes port 5432 internally |
| `k8s/configmap.yaml` | ConfigMap | Stores non-sensitive environment config (e.g., `DATABASE_HOST`, `API_URL`) |
| `k8s/secret.yaml` | Secret | Stores sensitive credentials (e.g., `DATABASE_URL`, `SUPABASE_KEY`) as base64-encoded values |
| `k8s/ingress.yaml` | Ingress | Routes external HTTP traffic to frontend and backend services based on path rules |
| `k8s/hpa.yaml` | HorizontalPodAutoscaler | Automatically scales the backend deployment between 2–10 replicas based on CPU utilization (≥ 70%) |

---

## 🔬 Wireshark Filter Reference

### Capture Filters (applied before capture starts)

| Filter | What It Captures |
|--------|-----------------|
| `port 8000` | All TCP traffic to/from the FastAPI backend |
| `port 3000` | All TCP traffic to/from the Next.js frontend |
| `host <railway-backend-ip>` | All packets to/from the Railway-deployed backend |
| `tcp port 443` | Encrypted HTTPS traffic to Railway/Supabase |
| `tcp port 5432` | PostgreSQL database queries (local Docker only) |

### Display Filters (applied after capture)

| Filter | What It Shows |
|--------|--------------|
| `http` | All unencrypted HTTP requests and responses |
| `http.request.method == "POST"` | Only POST requests (e.g., login, booking creation) |
| `http.request.method == "GET"` | Only GET requests (e.g., fetching rides, user profile) |
| `http.response.code == 200` | Successful responses |
| `http.response.code == 401` | Unauthorized responses (failed auth) |
| `http.response.code == 422` | Validation errors from FastAPI |
| `tcp.stream eq <N>` | Follow a specific TCP conversation end-to-end |
| `ip.addr == <backend-ip>` | Traffic to/from a specific IP (Railway backend) |
| `dns` | DNS lookups (e.g., resolving Railway hostnames) |
| `tls.handshake.type == 1` | TLS Client Hello — shows HTTPS connection initiation |

---

## 🌐 Live Deployment & Endpoints

| Service | URL |
|---------|-----|
| **Frontend (Railway)** | `https://campus-ride-frontend.up.railway.app` |
| **Backend API (Railway)** | `https://campus-ride-backend.up.railway.app` |
| **API Documentation** | `https://campus-ride-backend.up.railway.app/docs` |
| **API ReDoc** | `https://campus-ride-backend.up.railway.app/redoc` |

### Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/login` | Login with email & password |
| `POST` | `/auth/register` | Register a new user |
| `GET` | `/rides` | Get all available rides |
| `POST` | `/rides` | Create a new ride offer |
| `POST` | `/rides/{id}/book` | Book a ride |
| `GET` | `/users/me` | Get current user profile |
| `GET` | `/health` | Health check endpoint |

> 🔒 Most endpoints require a Bearer token in the `Authorization` header.

---

## 🛠️ Troubleshooting

### 1. `docker-compose up` fails — "port already in use"

**Symptom:** Error: `Bind for 0.0.0.0:5432 failed: port is already allocated`

**Cause:** A local PostgreSQL instance is already running on port 5432.

**Solution:**
```bash
# Stop the local PostgreSQL service:
# Windows:
net stop postgresql-x64-15
# Linux/macOS:
sudo service postgresql stop

# Then re-run:
docker-compose up --build
```

---

### 2. FastAPI returns `401 Unauthorized` on all requests

**Symptom:** Every API call returns `{"detail": "Could not validate credentials"}`

**Cause:** `SUPABASE_SERVICE_ROLE_KEY` or `SECRET_KEY` is wrong/missing in `.env`

**Solution:**
1. Double-check your `.env` file in the backend service directory
2. Ensure `SUPABASE_SERVICE_ROLE_KEY` is the **Service Role** key, not the Anon key
3. Restart the backend:
   ```bash
   docker-compose restart backend
   ```

---

### 3. Kubernetes pods stuck in `CrashLoopBackOff`

**Symptom:** `kubectl get pods` shows `CrashLoopBackOff` for backend pod

**Cause:** Secret/ConfigMap values are missing or incorrectly base64-encoded

**Solution:**
```bash
# Check pod logs:
kubectl logs <pod-name>

# Verify secret values (they must be base64-encoded):
echo -n "your_database_url" | base64

# Re-apply secrets after fixing:
kubectl delete -f k8s/secret.yaml
kubectl apply -f k8s/secret.yaml
kubectl rollout restart deployment/backend-deployment
```

---

### 4. Artillery load test shows `ECONNREFUSED`

**Symptom:** All Artillery requests fail with connection refused

**Cause:** Target URL in `load-test.yml` is pointing to `localhost` but the server isn't running, or the Railway URL is wrong

**Solution:**
1. Ensure the Railway backend is deployed and accessible via browser first
2. Update `load-test.yml` target to your correct Railway URL:
   ```yaml
   config:
     target: "https://campus-ride-backend.up.railway.app"
   ```
3. Check Railway deployment logs if the service is down

---

### 5. Next.js frontend shows "Network Error" on API calls

**Symptom:** Frontend loads but API requests fail in browser console

**Cause:** `NEXT_PUBLIC_API_URL` is not set correctly in `.env.local`

**Solution:**
1. Verify `frontend/.env.local` exists and has the correct backend URL
2. Restart the frontend dev server — Next.js does **not** hot-reload `.env.local` changes:
   ```bash
   # Stop the server, then:
   pnpm dev
   ```

---

## 👥 Team Member Contributions

| Name | Student ID | Parts Handled | Responsibilities |
|------|-----------|---------------|-----------------|
| Putri | [ID] | Part 1, 2, 8 | Project setup, FastAPI backend development, database schema, Supabase integration, troubleshooting documentation |
| Afrina | [ID] | Part 3, 4, 5 | Next.js frontend development, Docker Compose configuration, Kubernetes manifests, Minikube deployment, HPA configuration |
| Azmirah | [ID] | Part 6, 7 | Wireshark network captures, traffic analysis, Artillery load testing, performance analysis, report generation |

> ✏️ *Update Student IDs before submission.*

---

## 📁 Project Structure

```
dist-sys-app/
├── frontend/                   # Next.js frontend application
│   ├── next.config.ts
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── postcss.config.mjs
│   └── tsconfig.json
├── services/                   # Backend microservices
│   └── backend/                # FastAPI backend
├── k8s/                        # Kubernetes manifests
│   ├── backend.yaml
│   ├── configmap.yaml
│   ├── frontend.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── postgres.yaml
│   └── secret.yaml
├── supabase/
│   └── migrations/
│       └── 001_university_ride.sql   # Initial DB schema
├── docker-compose.yml          # Local multi-container setup
├── load-test.yml               # Artillery load test config
├── process.md                  # Development process notes
└── README.md                   # This file
```

---

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Railway Deployment Docs](https://docs.railway.app/)
- [Artillery Load Testing Docs](https://www.artillery.io/docs)
- [Wireshark User Guide](https://www.wireshark.org/docs/wsug_html/)

---

*STIJK2124 — Distributed Systems | Group Project | Universiti Utara Malaysia*
