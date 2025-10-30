# Docker Deployment Guide

Deploy Chess Tournament Monitor using Docker with persistent SQLite database.

## Why Docker + SQLite?

✅ **Simple** - No external database required
✅ **Portable** - Run anywhere (VPS, cloud, local)
✅ **Persistent** - Data stored in mounted volume
✅ **Self-contained** - Everything in one container
✅ **Cost-effective** - No database service fees
✅ **Production-ready** - Includes health checks & auto-restart

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/rathnakara/chessresults.git
cd chessresults
```

### 2. Build & Run with Docker Compose

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

That's it! App is now running at http://localhost:8080

## Manual Docker Commands

### Build Image

```bash
docker build -t chess-monitor .
```

### Run Container

```bash
# Create data directory for persistence
mkdir -p data

# Run container
docker run -d \
  --name chess-monitor \
  -p 8080:8080 \
  -v $(pwd)/data:/app/data \
  -e DATABASE_URL=sqlite:///data/sessions.db \
  --restart unless-stopped \
  chess-monitor
```

### Manage Container

```bash
# View logs
docker logs -f chess-monitor

# Stop container
docker stop chess-monitor

# Start container
docker start chess-monitor

# Remove container
docker rm -f chess-monitor

# Restart container
docker restart chess-monitor
```

## Data Persistence

### SQLite Database Location

- **Inside container**: `/app/data/sessions.db`
- **On host**: `./data/sessions.db`

The `data/` directory is mounted as a volume, so:
- ✅ Sessions survive container restarts
- ✅ Sessions survive image rebuilds
- ✅ Data persists on host machine
- ✅ Easy to backup (just copy `data/` folder)

### Backup Database

```bash
# Copy database file
cp data/sessions.db data/sessions.db.backup

# Or backup entire data directory
tar -czf chess-monitor-backup-$(date +%Y%m%d).tar.gz data/
```

### Restore Database

```bash
# Stop container
docker-compose down

# Restore database
cp data/sessions.db.backup data/sessions.db

# Start container
docker-compose up -d
```

## Deploy to Production

### Option 1: VPS/Cloud Server (DigitalOcean, AWS, etc.)

1. **Setup server** (Ubuntu 22.04 recommended)

2. **Install Docker:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

3. **Clone & Deploy:**
```bash
git clone https://github.com/rathnakara/chessresults.git
cd chessresults
docker-compose up -d
```

4. **Setup reverse proxy (Nginx):**
```bash
sudo apt install nginx

# Create nginx config
sudo nano /etc/nginx/sites-available/chess-monitor
```

Nginx config:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 300s;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/chess-monitor /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

5. **SSL with Certbot (optional but recommended):**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Option 2: Render with Docker

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: chess-tournament-monitor
    env: docker
    dockerfilePath: ./Dockerfile
    dockerContext: .
    plan: free
    disk:
      name: chess-data
      mountPath: /app/data
      sizeGB: 1
    envVars:
      - key: DATABASE_URL
        value: sqlite:///data/sessions.db
```

2. Deploy to Render:
   - Connect GitHub repo
   - Render auto-detects Docker
   - Add persistent disk for `/app/data`

### Option 3: Railway

1. **Install Railway CLI:**
```bash
npm i -g @railway/cli
```

2. **Deploy:**
```bash
railway login
railway init
railway up
```

3. **Add volume** in Railway dashboard:
   - Path: `/app/data`
   - Size: 1GB

### Option 4: AWS ECS/Fargate

1. Push image to ECR
2. Create ECS task with EFS volume
3. Mount `/app/data` to EFS

### Option 5: Docker Hub + Any Server

1. **Build & push to Docker Hub:**
```bash
docker build -t yourusername/chess-monitor .
docker push yourusername/chess-monitor
```

2. **Pull & run on any server:**
```bash
docker pull yourusername/chess-monitor
docker run -d -p 8080:8080 -v ./data:/app/data yourusername/chess-monitor
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///data/sessions.db` | Database connection URL |
| `PORT` | `8080` | Port to run the app |
| `DEBUG` | `false` | Enable debug mode |
| `TZ` | `Asia/Kolkata` | Timezone for timestamps and logs |

### Timezone Configuration

The container is pre-configured with **Asia/Kolkata (IST)** timezone. To change:

**Method 1: Environment Variable (Recommended)**

Edit `docker-compose.yml`:
```yaml
environment:
  - TZ=America/New_York  # Change to your timezone
```

Or with `docker run`:
```bash
docker run -d \
  -e TZ=America/New_York \
  -p 8080:8080 \
  -v $(pwd)/data:/app/data \
  chess-monitor
```

**Method 2: Mount Host Timezone**

Uncomment in `docker-compose.yml`:
```yaml
volumes:
  - /etc/localtime:/etc/localtime:ro
  - /etc/timezone:/etc/timezone:ro
```

**Common Timezones:**
- India: `Asia/Kolkata` (IST, UTC+5:30)
- USA East: `America/New_York` (EST/EDT, UTC-5/-4)
- USA West: `America/Los_Angeles` (PST/PDT, UTC-8/-7)
- UK: `Europe/London` (GMT/BST, UTC+0/+1)
- Germany/France: `Europe/Paris` (CET/CEST, UTC+1/+2)
- Japan: `Asia/Tokyo` (JST, UTC+9)
- Australia: `Australia/Sydney` (AEST/AEDT, UTC+10/+11)
- Singapore: `Asia/Singapore` (SGT, UTC+8)
- UAE: `Asia/Dubai` (GST, UTC+4)

**Verify timezone in container:**
```bash
docker exec chess-tournament-monitor date
# Should show your configured timezone
```

[Full timezone list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

## Health Checks

Docker includes automatic health checks:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/"]
  interval: 30s
  timeout: 10s
  retries: 3
```

Container status:
- **healthy** - App is running fine
- **unhealthy** - App is not responding (auto-restart)

Check health:
```bash
docker ps  # Shows health status
docker inspect chess-monitor | grep -A 10 Health
```

## Monitoring & Logs

### View logs:
```bash
# Real-time logs
docker logs -f chess-monitor

# Last 100 lines
docker logs --tail 100 chess-monitor

# Logs with timestamps
docker logs -t chess-monitor
```

### Container stats:
```bash
docker stats chess-monitor
```

### System resource usage:
```bash
docker system df
```

## Scaling

### Vertical Scaling (More Resources)

Limit container resources:
```bash
docker run -d \
  --name chess-monitor \
  --memory="1g" \
  --cpus="1.0" \
  -p 8080:8080 \
  -v $(pwd)/data:/app/data \
  chess-monitor
```

### Horizontal Scaling (Multiple Instances)

Use load balancer with multiple containers:

```yaml
# docker-compose.yml for scaling
version: '3.8'

services:
  chess-monitor:
    build: .
    ports:
      - "8080-8082:8080"  # 3 instances
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///data/sessions.db
    deploy:
      replicas: 3
```

Run:
```bash
docker-compose up -d --scale chess-monitor=3
```

**Note:** For scaling, consider using PostgreSQL instead of SQLite to avoid database locking issues.

## Troubleshooting

### Container won't start

```bash
# Check logs
docker logs chess-monitor

# Check if port is in use
lsof -i :8080

# Verify image was built
docker images | grep chess-monitor
```

### Database errors

```bash
# Check database file permissions
ls -la data/sessions.db

# Reset database
rm data/sessions.db
docker restart chess-monitor
```

### Data not persisting

```bash
# Verify volume mount
docker inspect chess-monitor | grep -A 10 Mounts

# Check data directory
ls -la data/
```

### High memory usage

```bash
# Check stats
docker stats chess-monitor

# Restart container
docker restart chess-monitor
```

## Maintenance

### Update Application

```bash
# Pull latest code
git pull origin master

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Clean Up

```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Full system cleanup
docker system prune -a
```

## Cost Comparison

| Platform | Cost | Database | Notes |
|----------|------|----------|-------|
| **VPS (DigitalOcean)** | $4-6/mo | SQLite (free) | Best value, full control |
| **AWS Lightsail** | $3.5/mo | SQLite (free) | Easy setup |
| **Railway** | Free tier | SQLite (free) | 500 hours/mo, 1GB storage |
| **Render (Docker)** | Free | SQLite (free) | Sleeps after 15 min |
| **Render (PostgreSQL)** | Free | Free (90 days) | No sleep, expires |

**Recommendation:** $5/mo VPS with Docker + SQLite = Best solution!

## Production Checklist

- [ ] Docker image built successfully
- [ ] Data volume mounted correctly
- [ ] Health checks passing
- [ ] Logs are accessible
- [ ] Backups configured
- [ ] Reverse proxy setup (if needed)
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Resource limits set
- [ ] Monitoring enabled

## Support

- **Docker issues**: Check Docker logs and documentation
- **App issues**: Check application logs in container
- **Database issues**: Verify volume mount and permissions

## Summary

✅ **3 commands to deploy:**
```bash
git clone https://github.com/rathnakara/chessresults.git
cd chessresults
docker-compose up -d
```

✅ **Data persists** in `./data/` directory
✅ **Auto-restarts** on failure
✅ **Production-ready** with health checks
✅ **Easy backups** - just copy `data/` folder
✅ **Cost-effective** - $4-6/mo on any VPS

Your chess tournament monitor is now containerized and ready to deploy anywhere! 🐳♟️
