"""
Run this file from the animal-detection folder:
    python run_dashboard.py

Then open:  http://127.0.0.1:5000
"""

import os
import glob
from flask import Flask, render_template, send_from_directory, jsonify

# ── Absolute paths (always correct no matter where you run from) ──────────────
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))          # animal-detection/
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
TMPL_DIR = os.path.join(ROOT_DIR, "dashboard", "dashboard", "templates")

print(f"[ROOT]  : {ROOT_DIR}")
print(f"[LOGS]  : {LOGS_DIR}  -> exists: {os.path.exists(LOGS_DIR)}")
print(f"[TMPLS] : {TMPL_DIR}  -> exists: {os.path.exists(TMPL_DIR)}")

os.makedirs(LOGS_DIR, exist_ok=True)

app = Flask(__name__, template_folder=TMPL_DIR)


# ── Helper ────────────────────────────────────────────────────────────────────
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


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    detections = parse_detections()
    print(f"  -> Rendering dashboard with {len(detections)} detection(s)")
    return render_template("index.html", detections=detections)


@app.route("/api/detections")
def api_detections():
    """JSON API – polled every 15 s by the browser for live updates."""
    return jsonify(parse_detections())


@app.route("/logs/<path:filename>")
def serve_log_image(filename):
    """Serve snapshot images directly from the logs/ folder."""
    return send_from_directory(LOGS_DIR, filename)


# ── Start ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n[Dashboard] http://127.0.0.1:5000\n")
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)
