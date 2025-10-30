# Chess Tournament Monitor

A simple Flask application to monitor chess tournament results in real-time for **multiple players simultaneously**.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open browser
# http://localhost:8080
```

## 📖 Features

- ✅ **Multiple player monitoring** - Monitor unlimited players at once
- ✅ Real-time tournament updates
- ✅ Live match results updates
- ✅ New round notifications
- ✅ Server-Sent Events for instant updates
- ✅ Individual session management
- ✅ Grid view for all sessions

## 📁 Project Structure

```
.
├── app.py                      # Main application (run this!)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── README_APP.md              # Detailed documentation
├── QUICKSTART_APP.md          # Quick start guide
├── templates/
│   ├── simple_index.html      # Home page - add players
│   ├── simple_view.html       # View all sessions (grid)
│   └── single_view.html       # View single session
└── src/                       # Core logic
    ├── api/                   # Chess-results.com API client
    ├── config.py              # Configuration
    ├── models/                # Data models
    ├── parsers/               # URL and HTML parsers
    └── services/              # Tournament monitoring service
```

## 📝 Usage

### Add Multiple Players

1. Go to http://localhost:8080
2. Enter first player's URL from [chess-results.com](https://chess-results.com)
3. Click "Start Monitoring"
4. Form resets - add another player's URL
5. Repeat for all players you want to monitor

### View All Sessions

- Go to http://localhost:8080/view
- See all players in a grid layout
- Real-time updates for each player
- Remove individual sessions with ✕ button

### View Single Session

- Click "View This Session" after adding
- Or go to http://localhost:8080/view/SESSION_ID
- Full detailed view of one player

## 🎯 Key Features

### Multi-Session Support
- Monitor unlimited players simultaneously
- Each session runs independently
- No limit on concurrent sessions

### Real-Time Updates
- Server-Sent Events (SSE) for instant updates
- Backup polling every 30 seconds
- Automatic reconnection on disconnect

### Session Management
- Add new sessions anytime
- Remove individual sessions
- View all sessions in grid layout
- View single session in detail

## 🔧 Requirements

- Python 3.8+
- Flask 3.0+
- requests
- beautifulsoup4

## 🌐 API Endpoints

- `POST /api/monitor` - Start monitoring a player
- `GET /api/sessions` - Get all active sessions
- `GET /api/status/<id>` - Get session status
- `GET /api/stream/<id>` - SSE stream for updates
- `POST /api/stop/<id>` - Stop monitoring a session

## 📚 Documentation

- See [README_APP.md](README_APP.md) for detailed documentation
- See [QUICKSTART_APP.md](QUICKSTART_APP.md) for quick start guide

## 📄 License

For personal use. Please respect chess-results.com's terms of service.
