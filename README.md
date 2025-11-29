# 🧹 Indoor Cleaning Robot – Intelligent Robotics Final Project

### *University of Birmingham – Group 38*

This repository implements a complete intelligent indoor cleaning robot system, including:

- 🏠 **Webots simulation environment**
- 🤖 **Python robot controller** (vision detection + obstacle avoidance + FSM)
- 🎯 **Supervisor for global position tracking**
- 🌐 **FastAPI backend (WebSocket-based)**
- 💻 **React frontend for real-time visualization**

---

## 1. 🚀 Project Overview

### Core Features

- Autonomous exploration & obstacle avoidance
- Red cleaning-zone detection using **HSV + Canny + Contours**
- Finite State Machine (**EXPLORE / CLEAN**)
- Cleaned zone marking (green dots)
- Real-time WebSocket pipeline
- Frontend visualization of trajectory, robot orientation, and cleaned zones

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

- HSV segmentation
- Canny edge detection
- Contour extraction
- Area thresholding

### navigation.py – Movement & obstacle avoidance  

- Forward movement
- Reactive avoidance

### behavior_fsm.py – Finite State Machine  

- EXPLORE  
- CLEAN  

### cleaner_controller.py – Main Loop  

- Capture camera frames  
- Run perception  
- Update FSM  
- Perform cleaning duration  
- Resume exploration  

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

- `/ws/supervisor`
- `/ws`

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

- Map boundary
- Robot trajectory
- Orientation triangle
- Cleaned dots
- State label

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

Visit <http://localhost:5173>
