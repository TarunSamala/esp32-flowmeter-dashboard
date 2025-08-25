# 🚀 ESP32 Flowmeter Dashboard

A **real-time React dashboard** for monitoring **five ESP32-S3 Sense cameras** connected to flowmeters.  
It fetches **live OCR readings** from your backend API, displays **live video streams**, and works **out of the box**.

---

## ✨ Features

- **5 Live Camera Feeds** — MJPEG streams from ESP32-S3 Sense  
- **Real-time OCR Readings** — Extracts numbers like `05766075` from flowmeters  
- **Demo Mode Fallback** — Works even if no backend is connected  
- **Single HTML File** — No build tools; just drop and run  
- **Mobile Friendly** — Fully responsive UI

---

## 📦 Installation

### Option 1 — Run Locally
```bash
git clone https://github.com/TarunSamala/esp32-flowmeter-dashboard.git
cd esp32-flowmeter-dashboard
```

### Option 2 — Deploy to GitHub Pages
1. Fork/clone this repo.
2. Push to your GitHub account.
3. In **Settings → Pages**, select the **main** branch and **/(root)** folder.
4. Your dashboard will be live at:
   `https://your-name.github.io/esp32-flowmeter-dashboard`

### Option 3 — Netlify/Vercel
Drag-and-drop the folder in Netlify, or point Vercel to this repo. No config needed.

---

## 🔌 API Endpoints

| Endpoint            | Method | Description                                  |
|--------------------|--------|----------------------------------------------|
| `/api/readings`    | GET    | Returns JSON data for current meter readings |
| `/stream/cam{1-5}` | GET    | MJPEG streams from ESP32-S3 cameras          |

**Example `/api/readings` Response**
```json
{
  "meters": [
    {
      "id": 1,
      "name": "ME Flowmeter",
      "reading": "05766075",
      "unit": "LITERS",
      "updatedAt": 1730200000000
    },
    {
      "id": 2,
      "name": "Boiler Flowmeter",
      "reading": "12345012",
      "unit": "LITERS",
      "updatedAt": 1730200000000
    }
  ]
}
```

---

## 🔧 Customization

**Change API Base URL** (if your backend is on a different host):  
Append a query param when opening the page:
```
index.html?apiBase=https://your-server.example.com
```

---

## 🧰 Tech Stack
- Frontend: React 18 via CDN
- Styling: Pure CSS (Tailwind-like utility design)
- OCR Engine (backend): Tesseract / OpenCV
- ESP32 Streaming: MJPEG over HTTP

---

## 📜 License
This project is licensed under the **MIT License**. You are free to use, modify, and distribute.

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Please open a PR or file an issue.

---

