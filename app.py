#!/usr/bin/env python3
"""
Chess Tournament Monitor - Multi-Session App
Simple Flask application to monitor chess tournaments for multiple players
Run: python app.py
"""

from flask import (
    Flask,
    request,
    Response,
    render_template,
    jsonify,
    stream_with_context,
)
import json
import threading
import queue
import uuid
from datetime import datetime
from typing import Dict, Optional
from src.config import Config
from src.api.client import ChessResultsClient
from src.parsers.url_parser import parse_chess_url
from src.services.monitor import TournamentMonitor
from src.models.tournament import Tournament
from src.database import Database

app = Flask(__name__, template_folder="./templates")

# Configuration
MAX_SESSIONS = 4

# Initialize database
db = Database()
db.create_tables()

# In-memory event queues (these don't need persistence)
event_queues: Dict[str, queue.Queue] = {}


def serialize_tournament(tournament: Tournament) -> dict:
    """Convert Tournament object to JSON-serializable dict"""
    return {
        "tournament_id": tournament.tournament_id,
        "player": {
            "name": tournament.player.name,
            "snr": tournament.player.snr,
            "starting_rank": tournament.player.starting_rank,
            "current_rank": tournament.player.current_rank,
        },
        "matches": [
            {
                "round_number": m.round_number,
                "board_number": m.board_number,
                "opponent_snr": m.opponent_snr,
                "opponent_name": m.opponent_name,
                "result": m.result,
                "pairing": m.pairing,
                "color": m.color,
                "is_completed": m.is_completed(),
            }
            for m in tournament.matches
        ],
        "total_rounds": tournament.total_rounds,
        "completed_rounds": tournament.get_completed_rounds(),
        "is_finished": tournament.is_finished(),
    }


def monitor_worker(session_id: str, config: Config, event_q: queue.Queue):
    """Background worker to monitor tournament"""
    print(f"🔧 Monitor worker starting for session: {session_id}")
    print(f"⚙️  Check interval: {config.check_interval}s")

    try:
        with ChessResultsClient(config) as client:
            monitor = TournamentMonitor(config, client)

            def on_update(tournament, new_round, error=None):
                """Callback when tournament updates"""
                session = db.get_session_by_id(session_id)
                if not session:
                    return

                # Handle error case
                if error:
                    print(f"⚠️  Monitor error [{session_id}]: {error}")
                    error_data = {
                        "error": error,
                        "timestamp": datetime.now().isoformat(),
                        "type": "fetch_error",
                    }
                    db.update_session(
                        session_id, last_update=datetime.now(), error=error
                    )
                    event_q.put(error_data)
                    return

                # Handle normal update
                if tournament:
                    print(
                        f"✅ Update [{session_id}] - Rounds: {tournament.get_completed_rounds()}/{tournament.total_rounds}"
                    )
                    data = serialize_tournament(tournament)
                    data["new_round"] = new_round is not None
                    data["timestamp"] = datetime.now().isoformat()

                    # Update session in database
                    db.update_session(session_id, data=data, last_update=datetime.now())
                    event_q.put(data)

            # Update session status
            db.update_session(session_id, status="running")
            print(f"▶️  Monitor started for session: {session_id}")

            # Run monitor
            monitor.run(callback=on_update)

            # Mark as finished
            db.update_session(session_id, status="finished")
            print(f"🏁 Monitor finished for session: {session_id}")

    except Exception as e:
        print(f"❌ Monitor error [{session_id}]: {e}")
        import traceback

        traceback.print_exc()
        db.update_session(session_id, status="error", error=str(e))
        event_q.put({"error": str(e), "type": "worker_error"})


def restart_existing_sessions():
    """Restart monitoring threads for existing sessions on app startup"""
    print("🔄 Checking for existing sessions to restart...")
    active_sessions = db.get_all_sessions()

    for session in active_sessions:
        # Skip finished or error sessions
        if session["status"] in ["finished", "error"]:
            continue

        session_id = session["id"]
        config_dict = session["config"]

        # Recreate Config object
        config = Config.from_env()
        config.tournament_id = config_dict["tournament_id"]
        config.player_snr = config_dict["player_snr"]
        config.server = config_dict["server"]
        config.federation = config_dict["federation"]
        config.check_interval = config_dict["check_interval"]

        # Create event queue
        event_queue = queue.Queue()
        event_queues[session_id] = event_queue

        # Restart monitoring thread
        thread = threading.Thread(
            target=monitor_worker, args=(session_id, config, event_queue), daemon=True
        )
        thread.start()
        print(f"✅ Restarted monitoring for session: {session_id}")

    if active_sessions:
        print(
            f"🔄 Restarted {len([s for s in active_sessions if s['status'] not in ['finished', 'error']])} monitoring sessions"
        )


@app.route("/")
def index():
    """Serve the main web page"""
    return render_template("simple_index.html")


@app.route("/api/monitor", methods=["POST"])
def start_monitor():
    """Start monitoring a tournament"""
    # Check session limit
    active_sessions = db.get_all_sessions()
    if len(active_sessions) >= MAX_SESSIONS:
        return jsonify(
            {
                "error": f"Maximum of {MAX_SESSIONS} sessions reached. Please stop a session before starting a new one."
            }
        ), 429

    data = request.json or {}
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Parse URL
    parsed = parse_chess_url(url)
    if not parsed:
        return jsonify({"error": "Invalid chess-results.com URL"}), 400

    # Create config
    config = Config.from_env()
    config.tournament_id = parsed["tournament_id"]
    config.player_snr = parsed["player_snr"]
    config.server = parsed["server"]
    config.federation = parsed["federation"]

    # Override check interval if provided
    check_interval = data.get("check_interval")
    if check_interval:
        config.check_interval = int(check_interval)

    # Create session
    session_id = str(uuid.uuid4())
    event_queue = queue.Queue()
    event_queues[session_id] = event_queue

    # Save session to database
    db.create_session(
        session_id,
        url,
        {
            "tournament_id": config.tournament_id,
            "player_snr": config.player_snr,
            "server": config.server,
            "federation": config.federation,
            "check_interval": config.check_interval,
        },
    )

    # Start monitoring in background thread
    thread = threading.Thread(
        target=monitor_worker, args=(session_id, config, event_queue), daemon=True
    )
    thread.start()

    return jsonify(
        {
            "session_id": session_id,
            "message": "Monitoring started",
        }
    )


@app.route("/api/sessions", methods=["GET"])
def get_sessions():
    """Get all active monitoring sessions"""
    active_sessions = db.get_all_sessions()
    return jsonify(
        {
            "sessions": [
                {
                    "id": session["id"],
                    "status": session["status"],
                    "created_at": session["created_at"].isoformat(),
                    "last_update": session["last_update"].isoformat()
                    if session["last_update"]
                    else None,
                    "config": session["config"],
                }
                for session in active_sessions
            ]
        }
    )


@app.route("/api/status/<session_id>", methods=["GET"])
def get_status(session_id):
    """Get current status of a specific monitoring session"""
    session = db.get_session_by_id(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    return jsonify(
        {
            "session_id": session["id"],
            "status": session["status"],
            "created_at": session["created_at"].isoformat(),
            "last_update": (
                session["last_update"].isoformat() if session["last_update"] else None
            ),
            "data": session["data"],
            "error": session.get("error"),
        }
    )


@app.route("/api/stream/<session_id>", methods=["GET"])
def stream_events(session_id):
    """Server-Sent Events stream for real-time updates"""
    session = db.get_session_by_id(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    if session_id not in event_queues:
        return jsonify({"error": "Event queue not found"}), 404

    event_queue = event_queues[session_id]

    @stream_with_context
    def generate():
        """Generate SSE events"""
        # Send initial connection message
        yield f'data: {{"type": "connected", "session_id": "{session_id}"}}\n\n'

        last_heartbeat = datetime.now()
        heartbeat_interval = 15
        heartbeat_count = 0

        while True:
            try:
                # Calculate timeout until next heartbeat
                time_since_heartbeat = (datetime.now() - last_heartbeat).total_seconds()
                timeout = max(1, heartbeat_interval - time_since_heartbeat)

                # Wait for events with timeout
                data = event_queue.get(timeout=timeout)
                yield f"data: {json.dumps(data)}\n\n"
                last_heartbeat = datetime.now()

                # Check if session is finished
                session = db.get_session_by_id(session_id)
                if session and session["status"] in ["finished", "error"]:
                    break

            except queue.Empty:
                # Send heartbeat
                heartbeat_count += 1
                yield ": heartbeat\n\n"
                last_heartbeat = datetime.now()

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.route("/api/stop/<session_id>", methods=["POST"])
def stop_monitor(session_id):
    """Stop a specific monitoring session"""
    session = db.get_session_by_id(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    # Remove session from database
    db.delete_session(session_id)

    # Remove event queue
    if session_id in event_queues:
        del event_queues[session_id]

    return jsonify({"message": "Monitoring stopped"})


@app.route("/view")
def view_all_sessions():
    """View all monitoring sessions"""
    return render_template("simple_view.html")


@app.route("/view/<session_id>")
def view_single_session(session_id):
    """View a specific monitoring session"""
    session = db.get_session_by_id(session_id)
    if not session:
        return "Session not found. Please start monitoring from the home page."

    return render_template("single_view.html", session_id=session_id)


# Error handlers
@app.errorhandler(404)
def error404(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def error500(error):
    return jsonify({"error": "Internal server error"}), 500


def main():
    """Run the web server"""
    import os

    # Get host and port from environment (for Render) or use defaults
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("DEBUG", "False").lower() == "true"

    # Restart existing sessions from database
    restart_existing_sessions()

    print("=" * 70)
    print("♟️  Chess Tournament Monitor - Multi-Session")
    print("=" * 70)
    print(f"Server starting on {host}:{port}")
    print("=" * 70)
    print("\nEndpoints:")
    print(f"  • Web UI:          http://{host}:{port}/")
    print(f"  • View All:        http://{host}:{port}/view")
    print(f"  • Start monitor:   POST http://{host}:{port}/api/monitor")
    print(f"  • Get sessions:    GET http://{host}:{port}/api/sessions")
    print(f"  • Get status:      GET http://{host}:{port}/api/status/<id>")
    print(f"  • Live stream:     GET http://{host}:{port}/api/stream/<id>")
    print(f"  • Stop monitor:    POST http://{host}:{port}/api/stop/<id>")
    print("=" * 70)
    print("\nFeatures:")
    print(f"  ✓ Multi-player monitoring (max {MAX_SESSIONS} concurrent sessions)")
    print("  ✓ Real-time updates via Server-Sent Events")
    print("  ✓ Automatic polling every 30 seconds")
    print("  ✓ Independent session management")
    print("  ✓ 2x2 grid layout optimized for 4 players")
    print("=" * 70)
    print("\nPress Ctrl+C to stop the server\n")

    app.run(host=host, port=port, debug=debug, use_reloader=False, threaded=True)


if __name__ == "__main__":
    main()
