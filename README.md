# ASWAMEDHA’26 – Capture The Flag Display Server

This repository contains the **Flask-based display and control server** developed for the **Capture The Flag (CTF)** event conducted during **ASWAMEDHA’26**.

The server provides:
- A **public display interface** for the CTF countdown timer
- An **admin interface** to control the timer
- **Authenticated REST APIs** to start, stop, reset, and sync the event timer

---

## 🧠 Project Overview

This application was designed to manage and display a **centralized, authoritative countdown timer** for a live CTF event.

### Key Capabilities
- ⏱️ 2-hour default CTF timer (configurable)
- 🌐 Public API for real-time timer status
- 🔐 API-key–protected admin endpoints
- 💾 Persistent timer state using JSON storage
- 📡 Client–server time drift correction
- 🖥️ Flask-rendered HTML views (`index.html`, `admin.html`)

---

## 🛠️ Tech Stack

- **Python 3**
- **Flask**
- **Flask-CORS**
- **HTML / CSS / JavaScript**
- JSON-based persistence (no database required)

---

## 📂 Project Structure
```
.
├── app.py
├── timer_state.json
├── templates/
│   ├── index.html
│   └── admin.html
└── README.md
```

---

## 🚀 How to Run the Server

### 1️⃣ Prerequisites

- Python **3.8+**
- `pip` installed

---

### 2️⃣ Install Dependencies

```bash
pip install flask flask-cors
```

---

### 3️⃣ Run the Server

```bash
python app.py
```

The server will start on:

```
http://localhost:5009
```

---

## 🌐 Available Routes

### Web Pages
| Route | Description |
|------|------------|
| `/` | Public CTF timer display |
| `/admin` | Admin control panel |

---

### API Endpoints

#### Public
```http
GET /api/timer/status
```

#### Authenticated (Header required)

```
X-API-Key: ctf_admin_2026_ashwamedha
```

| Method | Endpoint | Description |
|------|---------|------------|
| POST | `/api/timer/start` | Start the timer |
| POST | `/api/timer/stop` | Stop the timer |
| POST | `/api/timer/reset` | Reset timer |
| POST | `/api/timer/sync` | Sync timer |
| POST | `/api/timer/set-duration` | Set custom duration |

---

## 🔐 Security Notes

This server was designed for a **controlled event environment**.  
For production use:
- Use environment variables
- Disable debug mode
- Enable HTTPS

---

## 📄 License

**MIT License**

This project is open-source and free to use, modify, and distribute.

---

## 👨‍💻 Author

**Gokul P**  
GitHub: https://github.com/pgokul695
