# 🧹 Indoor Cleaning Robot – Intelligent Robotics Final Project

### *University of Birmingham – Group 38*

GitHub Repository: [https://github.com/ChrisWu11/Intelligent-Robotics-Final-Project-Group38](https://github.com/ChrisWu11/Intelligent-Robotics-Final-Project-Group38)

This repository implements a complete intelligent indoor cleaning robot system, including:

* 🏠 **Webots simulation environment**
* 🤖 **Python robot controller** (vision detection + obstacle avoidance + FSM)
* 🎯 **Supervisor for global position tracking**
* 🌐 **FastAPI backend (WebSocket-based)**
* 💻 **React frontend for real-time visualization**

---

## 1. 🚀 Project Overview

### Core Features

* Autonomous exploration & obstacle avoidance
* Red cleaning-zone detection using **HSV + Canny + Contours**
* Finite State Machine (**EXPLORE / CLEAN**)
* Cleaned zone marking (green dots)
* Real-time WebSocket pipeline
* Frontend visualization of trajectory, robot orientation, and cleaned zones

---

## 2. 🧩 System Architecture

```
Webots Robot Controller
        ↓
Supervisor (global pose)
        ↓
FastAPI Backend (WebSocket)
        ↓
Frontend (React)
```

---

## 3. 📁 Project Structure

```
project/
│
├── webots/
│   ├── worlds/apartment.wbt
│   ├── controllers/
│       ├── cleaner_controller/
│       │   ├── cleaner_controller.py
│       │   ├── navigation.py
│       │   ├── perception.py
│       │   ├── behavior_fsm.py
│       ├── monitor_supervisor/
│           └── monitor_supervisor.py
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│
└── frontend/
    ├── src/App.jsx
    ├── package.json
    └── public/
```

---

## 4. 🏡 Webots Simulation

The Webots world includes a furnished apartment, red cleaning zones, an E-puck robot with a custom controller, and a supervisor streaming position and rotation via WebSocket.

---

## 5. 🤖 Robot Controller (Python)

### perception.py – Red-zone detection

* HSV segmentation
* Canny edge detection
* Contour extraction
* Area thresholding

### navigation.py – Movement & obstacle avoidance

* Forward movement
* Reactive avoidance

### behavior_fsm.py – Finite State Machine

* EXPLORE
* CLEAN

### cleaner_controller.py – Main Loop

* Capture camera frames
* Run perception
* Update FSM
* Perform cleaning duration
* Resume exploration

---

## 6. 📡 Supervisor

Sends messages every 0.1s:

```json
{
  "event": "position",
  "x": -4.2,
  "y": -1.7,
  "z": 0.01,
  "ry": 1.25
}
```

---

## 7. 🌐 Backend (FastAPI + WebSocket)

Two WebSocket endpoints:

* `/ws/supervisor`
* `/ws`

Example broadcast:

```json
{
  "supervisor_x": -4.20,
  "supervisor_y": -1.73,
  "state": "CLEAN",
  "cleaned_zones": []
}
```

---

## 8. 💻 Frontend (React)

Displays:

* Map boundary
* Robot trajectory
* Orientation triangle
* Cleaned dots
* State label

---

## ⚠️ Important Notes

### Webots Python Dependencies

Webots does **not** include some Python libraries by default (e.g., `websocket`, `threading`).
You must install these dependencies into the **Python environment used by Webots**, otherwise the simulation will raise import errors.

To find Webots' Python path:

```
which python3
```

and install dependencies:

```
pip install websocket-client
```

### Frontend Node Version Requirement

The frontend requires **Node.js v20 or above**. Using older versions may cause build or runtime errors.

---

## 9. ▶️ Running the System

### 1️⃣ Backend

```
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8765 --reload
```

### 2️⃣ Webots

Open apartment.wbt and start simulation.

### 3️⃣ Frontend

```
cd frontend
npm install
npm run dev
```

Visit [http://localhost:5173](http://localhost:5173)
