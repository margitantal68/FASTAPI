# Module10: Deployment & CI/CD

## App's structure

In this module we dockerize the apps developed in module 6.
First of all, we create copies of the following modules: `module6_security` and `module6_frontend`.

1. Create the following structure:

```bash
module10_deployment_ci_cd/
├── backend
├── frontend
```

2. Copy the `module6_security` into `backend` folder
```bash
cp -r module6_security/*  module10_deployment_ci_cd/backend
```

3. Copy the `module6_frontend` into `frontend` folder
```bash 
cp -r module6_frontend/*  module10_deployment_ci_cd/frontend
```
You should see the following structure:

```bash
module10_deployment_ci_cd/
├── backend/         # FastAPI backend
├── frontend/
│   └── my-app/      # React + Vite frontend
```
4. Start the backend

```bash
cd backend
source .venv/bin/activate
```

```bash
uvicorn main:app --reload
```

5. Start the frontend

```bash
cd frontend/my-app
npm run dev
```
6. **Don't forget to stop both frontend and backend**

## Docker Files

Create Docker files:
- Backend Dockerfile → FastAPI + Uvicorn
- Frontend Dockerfile → React + Vite build, served with Nginx
- docker-compose.yml → Spins up backend, frontend, and Postgres

### Backend Dockerfile (module10_deployment_ci_cd/backend/Dockerfile)
```bash
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile (module10_deployment_ci_cd/frontend/my-app/Dockerfile)


```bash
# Build stage
FROM node:18-alpine AS build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

# Serve stage
FROM nginx:alpine

# Copy built files to nginx's HTML folder
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx config if needed
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```
### Docker Compose (docker-compose.yml) in root of module10_deployment_ci_cd/
```bash
version: "3.9"

services:
  db:
    image: postgres:15
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres123!
      - POSTGRES_DB=fastapi_week10
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5440:5432"
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres123!@db:5440/fastapi_week10
    depends_on:
      - db

  frontend:
    build: ./frontend/my-app
    ports:
      - "3000:80"
    depends_on:
      - backend



volumes:
  postgres_data:

```

## GitHub `OAuth app` registration
✅ Step-by-Step: Register an `OAuth App` on GitHub

1. Go to GitHub Developer Settings

Open your browser and go to: https://github.com/settings/developers

2. Choose "OAuth Apps"

On the left-hand sidebar, under "Developer settings", click on "OAuth Apps".

3. Click "New OAuth App"

You'll see a list (if any exist) and a button to "New OAuth App". Click it.

4. Fill Out the OAuth Application Form

Here’s what each field means:
- Field	Description
  - Application name:	Name of your app (e.g., MyCoolApp)
  - Homepage URL: `http://localhost:3000`
  - Authorization callback URL: `http://localhost:8000/auth/github/callback`

5. Click "Register application"

🎉 After Registration

Once registered, GitHub will give you:
- `Client ID` – Public identifier of your app
- `Client Secret` – Keep this secret! Used to authenticate your app

You’ll use these values when implementing OAuth in your app.

## Backend 

- `.env`: update  `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET` with the previously obtained values

```bash
DB_USER=
DB_PASS=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
JWT_SECRET_KEY="your_secret_key"
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

- `main.py`: Allow requests from `http://localhost:3000` too.

```python
# Allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",  "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```


- `auth.py`: Update `FRONTEND_REDIRECT_URL`

```python
FRONTEND_REDIRECT_URL = "http://localhost:3000/oauth/callback"
```

- `database.py`: Update `SQLALCHEMY_DATABASE_URL` - your database is available at service `@db` instead of `@localhost`

```python
SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@db/fastapi_week10'
```
## Frontend

- Create `nginx.conf` file in `module10_deployment_ci_cd/frontend/my-app`
```bash
server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri /index.html;
    }
}
```

## Start

```bash
docker compose up --build
```

- Backend → http://localhost:8000
- Frontend → http://localhost:3000
- Postgres → localhost:5440
