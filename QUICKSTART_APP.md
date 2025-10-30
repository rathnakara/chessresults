# Quick Start Guide

## Run in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
python app.py
```

### Step 3: Open Browser
Open: **http://localhost:8080**

---

## That's it! 🎉

You should see:
```
======================================================================
♟️  Chess Tournament Monitor - Single Player
======================================================================
Server starting on http://localhost:8080
======================================================================

Endpoints:
  • Web UI:        http://localhost:8080/
  • View Live:     http://localhost:8080/view
  • Start monitor: POST http://localhost:8080/api/monitor
  • Get status:    GET http://localhost:8080/api/status
  • Live stream:   GET http://localhost:8080/api/stream
  • Stop monitor:  POST http://localhost:8080/api/stop
======================================================================

Features:
  ✓ Single player monitoring
  ✓ Real-time updates via Server-Sent Events
  ✓ Automatic polling every 30 seconds
======================================================================

Press Ctrl+C to stop the server
```

## Usage

1. Enter your chess-results.com player URL
2. Click "Start Monitoring"
3. Click "View Live Updates"
4. Watch your tournament progress in real-time!

---

**Need help?** See [README_APP.md](README_APP.md) for full documentation.
