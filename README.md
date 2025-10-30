# Chess Tournament Monitor 🐳

A Docker-based Flask application to monitor chess tournament results in real-time for **multiple players simultaneously** with persistent SQLite database.

## 🚀 Quick Start (3 Commands!)

```bash
git clone https://github.com/rathnakara/chessresults.git
cd chessresults
docker-compose up -d
```

**Open:** http://localhost:8080

That's it! Your chess tournament monitor is running with persistent storage.

## 🎯 Features

- ✅ **Multiple player monitoring** - Track unlimited players simultaneously
- ✅ **Real-time updates** - Live tournament results via Server-Sent Events
- ✅ **Persistent storage** - SQLite database with Docker volume
- ✅ **Auto-restart** - Monitoring resumes after container restart
- ✅ **Production-ready** - Health checks & optimized for deployment
- ✅ **Docker-based** - Deploy anywhere (VPS, cloud, local)
- ✅ **Cost-effective** - No external database needed

## 📦 What's Included

```
.
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # One-command deployment
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── data/                   # SQLite database (persistent volume)
├── src/                    # Core application logic
│   ├── api/               # Chess-results.com API client
│   ├── config.py          # Configuration management
│   ├── database.py        # SQLite database handler
│   ├── models/            # Data models
│   ├── parsers/           # URL and HTML parsers
│   └── services/          # Tournament monitoring service
└── templates/             # HTML templates
    ├── simple_index.html  # Home page - add players
    ├── simple_view.html   # View all sessions (grid)
    └── single_view.html   # View single session
```

## 🎮 Usage

### Start the App

```bash
docker-compose up -d
```

### Add Players to Monitor

1. Go to http://localhost:8080
2. Paste tournament URL from [chess-results.com](https://chess-results.com)
3. Click "Start Monitoring"
4. Add more players (repeat)

### View All Sessions

- Go to http://localhost:8080/view
- See all players in grid layout
- Real-time updates for each player
- Remove sessions with ✕ button

### View Logs

```bash
docker-compose logs -f
```

### Stop the App

```bash
docker-compose down
```

## 📊 Data Persistence

Your data is stored in `./data/sessions.db` and persists across:
- ✅ Container restarts
- ✅ System reboots
- ✅ Image rebuilds
- ✅ Updates/deployments

**Backup your data:**
```bash
cp data/sessions.db data/sessions.db.backup
```

## 🌐 Deploy to Production

### Option 1: VPS ($4-6/month) ⭐ Recommended

Perfect for 24/7 monitoring with no limits.

**DigitalOcean, Linode, Vultr, AWS Lightsail:**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone and deploy
git clone https://github.com/rathnakara/chessresults.git
cd chessresults
docker-compose up -d
```

**Setup domain (optional):**
- Point DNS to your VPS IP
- Setup Nginx reverse proxy
- Add SSL with Let's Encrypt

### Option 2: Railway

```bash
railway login
railway init
railway up
```

Add volume in Railway dashboard: `/app/data` (1GB)

### Option 3: Render

- Connect GitHub repository
- Render auto-detects Docker
- Add persistent disk for `/app/data`
- Deploy!

### Option 4: Any Server with Docker

```bash
docker pull rathnakara/chessresults  # (if you publish to Docker Hub)
docker run -d -p 8080:8080 -v ./data:/app/data rathnakara/chessresults
```

**📖 Full deployment guide:** See [DOCKER_DEPLOY.md](DOCKER_DEPLOY.md)

## 🔧 Development

### Local Development (without Docker)

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create data directory
mkdir -p data

# Run app
python app.py
```

### Build Docker Image

```bash
docker build -t chess-monitor .
```

### Run with Custom Port

```bash
docker run -d -p 3000:8080 -v ./data:/app/data chess-monitor
```

## 🔍 API Endpoints

- `POST /api/monitor` - Start monitoring a player
- `GET /api/sessions` - Get all active sessions
- `GET /api/status/<id>` - Get session status
- `GET /api/stream/<id>` - SSE stream for live updates
- `POST /api/stop/<id>` - Stop monitoring a session

## 🛠️ Technology Stack

- **Backend:** Python 3.11, Flask
- **Database:** SQLite with SQLAlchemy
- **Web Server:** Gunicorn
- **Real-time:** Server-Sent Events (SSE)
- **Container:** Docker
- **Frontend:** Vanilla JavaScript, HTML/CSS

## 📋 Requirements

- Docker & Docker Compose (for containerized deployment)
- OR Python 3.8+ (for local development)

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///data/sessions.db` | Database connection |
| `PORT` | `8080` | Port to run the app |
| `DEBUG` | `false` | Enable debug mode |

## 🐛 Troubleshooting

### Container won't start

```bash
docker logs chess-tournament-monitor
```

### Reset database

```bash
docker-compose down
rm data/sessions.db
docker-compose up -d
```

### Port already in use

```bash
# Change port in docker-compose.yml
ports:
  - "3000:8080"  # Use port 3000 instead
```

### View container stats

```bash
docker stats chess-tournament-monitor
```

## 🎯 Why Docker + SQLite?

| Feature | This App | Other Solutions |
|---------|----------|-----------------|
| **Setup** | 3 commands | Complex database setup |
| **Cost** | $4-6/mo (VPS) | $20+/mo (managed DB) |
| **Portability** | Run anywhere | Tied to platform |
| **Maintenance** | Minimal | Database management |
| **Backups** | Copy one file | Complex procedures |
| **Persistence** | ✅ Yes | Often lost |

## 📝 License

For personal use. Please respect [chess-results.com](https://chess-results.com)'s terms of service.

## 🤝 Contributing

This is a personal project, but feel free to fork and modify for your needs!

## 📧 Support

- **Issues:** Open an issue on GitHub
- **Docker Help:** See [DOCKER_DEPLOY.md](DOCKER_DEPLOY.md)
- **Chess Results:** Visit [chess-results.com](https://chess-results.com)

## 🎉 Quick Recap

```bash
# 1. Clone
git clone https://github.com/rathnakara/chessresults.git
cd chessresults

# 2. Run
docker-compose up -d

# 3. Use
open http://localhost:8080
```

**Your chess tournament monitor is ready!** 🏆♟️
