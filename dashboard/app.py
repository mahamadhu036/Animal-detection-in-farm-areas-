from flask import Flask, render_template, send_from_directory, jsonify
import os
import glob

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # animal-detection/
LOGS_DIR = os.path.join(BASE_DIR, "logs")
TMPL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard", "templates")

app = Flask(__name__, template_folder=TMPL_DIR)

# ── Helper ─────────────────────────────────────────────────────────────────────
def parse_detections():
    """Return list of detection dicts parsed from log filenames."""
    files = glob.glob(os.path.join(LOGS_DIR, "*.jpg"))
    files = sorted(files, reverse=True)[:50]
    detections = []
    for f in files:
        name   = os.path.basename(f)
        parts  = name.replace(".jpg", "").split("_")
        animal = parts[0] if len(parts) > 0 else "unknown"
        date   = parts[1] if len(parts) > 1 else ""
        time_  = parts[2].replace("-", ":") if len(parts) > 2 else ""
        detections.append({
            "filename": name,
            "animal":   animal,
            "date":     date,
            "time":     time_,
        })
    return detections

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    detections = parse_detections()
    return render_template("index.html", detections=detections)

@app.route("/api/detections")
def api_detections():
    """JSON endpoint – polled by the dashboard for live updates."""
    return jsonify(parse_detections())

@app.route("/logs/<path:filename>")
def serve_log_image(filename):
    """Serve snapshot images stored in the logs/ folder."""
    return send_from_directory(LOGS_DIR, filename)

# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(LOGS_DIR, exist_ok=True)
    print(f"📂 Serving logs from: {LOGS_DIR}")
    print("🌐 Dashboard → http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)