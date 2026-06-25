# 🌾 Farm Animal Detection System

> Real-time AI-powered livestock & wildlife intrusion monitoring using YOLOv8 + Flask + Telegram

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?logo=flask)
![Telegram](https://img.shields.io/badge/Alerts-Telegram_Bot-blue?logo=telegram)

---

## 📌 Overview

This system uses a webcam + YOLOv8 to detect animals (birds, cats, dogs, cows, elephants, etc.) in real time. On detection it:

- 📸 **Saves a JPEG snapshot** to `logs/`
- 📲 **Sends a Telegram alert** to the farm owner instantly
- 🌐 **Displays all events** on a live web dashboard at `http://localhost:5000`

---

## 🗂️ Project Structure

```
animal-detection/
├── main.py              # 🎥 Detection engine (webcam + YOLO + alerts)
├── alert.py             # 📲 Telegram alert dispatcher
├── config.py            # ⚙️  Telegram credentials (TOKEN + CHAT_ID)
├── run_dashboard.py     # 🌐 Flask web dashboard server
├── yolov8n.pt           # 🧠 YOLOv8 nano model weights (~6 MB)
├── logs/                # 📁 Auto-saved detection snapshots
└── dashboard/
    ├── app.py           # Alternate Flask entry point
    ├── test_telegram.py # 🧪 Test Telegram connectivity
    └── dashboard/
        └── templates/
            └── index.html  # 🖥️ Live web dashboard UI
```

---

## 🦾 Detected Animals (COCO Classes)

| Animal | COCO ID | Category |
|--------|---------|----------|
| Bird | 14 | Bird / Pest |
| Cat | 15 | Stray |
| Dog | 16 | Stray |
| Horse | 17 | Livestock |
| Sheep | 18 | Livestock |
| Cow | 19 | Livestock |
| Elephant | 20 | Wild |
| Bear | 21 | Wild |
| Zebra | 22 | Wild |
| Giraffe | 23 | Wild |

---

## ⚙️ Setup & Installation

### 1. Install Dependencies
```bash
pip install ultralytics opencv-python flask requests
```

### 2. Configure Telegram
Edit `config.py`:
```python
TELEGRAM_TOKEN   = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
```
> Get your bot token from [@BotFather](https://t.me/BotFather) on Telegram.

### 3. Test Telegram Connectivity
```bash
cd dashboard
python test_telegram.py
```

---

## 🚀 Running the System

Run **both** in separate terminals from the `animal-detection/` directory:

**Terminal 1 — Detection Engine:**
```bash
python main.py
```

**Terminal 2 — Web Dashboard:**
```bash
python run_dashboard.py
```

Then open your browser at: **http://127.0.0.1:5000**

---

## 🌐 Web Dashboard Features

- 📊 Live stats: total detections, last detected animal, alert status
- 🖼️ Image grid of recent detection snapshots
- 📋 Full detection log table with date, time, and animal category
- ⏱️ Auto-refreshes every **15 seconds** without page reload
- 🟢 Animated LIVE indicator with real-time clock

---

## 📲 Alert Format (Telegram)

```
🚨 Farm Alert!
🐾 Animal: CAT
🕐 Time: 2026-06-25_20-11-30
```

Alerts have a **60-second cooldown per animal** to prevent spam.

---

## 🔌 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Live dashboard (HTML) |
| `GET /api/detections` | JSON list of detections (last 50) |
| `GET /logs/<filename>` | Serve snapshot image |

---

## 🛠️ Tech Stack

- **Python · YOLOv8 · OpenCV · Flask · Telegram Bot API**

---

## 📄 License

This project is for academic and educational use.
