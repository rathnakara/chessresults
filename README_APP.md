# Chess Tournament Monitor - Simple App

A simple single-file Flask application to monitor chess tournament results in real-time.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
python app.py
```

### 3. Open in Browser

Navigate to: **http://localhost:8080**

## 📖 How to Use

1. **Get your tournament URL**
   - Go to [chess-results.com](https://chess-results.com)
   - Find your tournament
   - Navigate to your player page
   - Copy the URL (should look like: `https://s1.chess-results.com/tnr1280521.aspx?lan=1&art=9&fed=IND&snr=126&SNode=S0`)

2. **Start Monitoring**
   - Paste the URL in the form
   - Optionally adjust the check interval (default: 30 seconds)
   - Click "Start Monitoring"

3. **View Live Updates**
   - Click "View Live Updates" to see real-time tournament data
   - New rounds will be highlighted automatically
   - Match results update in real-time

4. **Stop Monitoring**
   - Click "Stop Monitoring" button on the live view page
   - Or simply close the browser

## 📁 File Structure

```
.
├── app.py                          # Main application file (run this!)
├── requirements.txt                # Python dependencies
├── templates/
│   ├── simple_index.html          # Home page form
│   └── simple_view.html           # Live monitoring view
├── src/                           # Core logic (don't modify)
│   ├── config.py
│   ├── api/
│   │   └── client.py
│   ├── models/
│   │   └── tournament.py
│   ├── parsers/
│   │   ├── url_parser.py
│   │   └── tournament_parser.py
│   └── services/
│       └── monitor.py
└── README_APP.md                  # This file
```

## 🎯 Features

- ✅ **Single Player Monitoring** - Focus on one player at a time
- ✅ **Real-time Updates** - Uses Server-Sent Events for live data
- ✅ **Automatic Polling** - Checks for updates every 30 seconds (configurable)
- ✅ **New Round Alerts** - Highlights when new pairings are available
- ✅ **Match Results** - Shows all rounds with results
- ✅ **Simple Setup** - Just one command to run

## 🔧 Configuration

You can adjust the check interval when starting monitoring:
- Minimum: 5 seconds
- Maximum: 300 seconds (5 minutes)
- Default: 30 seconds

## 🌐 API Endpoints

If you want to use the API directly:

### Start Monitoring
```bash
curl -X POST http://localhost:8080/api/monitor \
  -H "Content-Type: application/json" \
  -d '{"url": "YOUR_TOURNAMENT_URL", "check_interval": 30}'
```

### Get Status
```bash
curl http://localhost:8080/api/status
```

### Stop Monitoring
```bash
curl -X POST http://localhost:8080/api/stop
```

### Stream Events (SSE)
```bash
curl http://localhost:8080/api/stream
```

## 🐛 Troubleshooting

**Problem: Port 8080 already in use**
- Edit `app.py` and change the port number in the last line:
  ```python
  app.run(host="localhost", port=8081, ...)  # Changed to 8081
  ```

**Problem: Module not found errors**
- Make sure you installed dependencies:
  ```bash
  pip install -r requirements.txt
  ```

**Problem: Invalid URL error**
- Make sure your URL is from chess-results.com
- URL must include the `snr` parameter (player serial number)
- Example: `https://s1.chess-results.com/tnr1280521.aspx?lan=1&art=9&fed=IND&snr=126&SNode=S0`

**Problem: No data showing**
- Check that the tournament is active
- Verify the player SNR is correct
- Check the console output for error messages

## 📝 Requirements

- Python 3.8+
- Flask 3.0+
- requests
- beautifulsoup4

All dependencies are listed in `requirements.txt`.

## 🎨 Customization

### Change Check Interval Default
Edit `app.py` line 223:
```python
value="30"  # Change to your preferred default
```

### Change Port
Edit `app.py` last line:
```python
app.run(host="localhost", port=8080, ...)  # Change port here
```

### Disable Debug Mode
Edit `app.py` last line:
```python
app.run(..., debug=False, ...)
```

## 📄 License

This project is for personal use. Please respect chess-results.com's terms of service and don't abuse their servers with too frequent requests.

## 🙏 Credits

Data provided by [chess-results.com](https://chess-results.com)
