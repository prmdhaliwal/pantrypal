# PantryPal AI

Recipe recommendations from ingredients you already have.

## Run With Docker

Prerequisite: Docker Desktop must be running.

Start the full app from the repository root:

```powershell
docker compose up --build
```

Open the frontend at:

```text
http://127.0.0.1:8080
```

The frontend sends backend requests through `/api`, which is proxied to the
backend service inside Docker Compose.

Stop the app:

```powershell
docker compose down
```
