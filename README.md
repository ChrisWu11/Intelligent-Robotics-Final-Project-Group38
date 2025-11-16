# 🧹 Indoor Cleaning Robot – Webots Simulation Project

## 🧠 Overview

This project explores **autonomous indoor cleaning** using a simulated robot in **Webots**.
The robot autonomously navigates a cluttered room, avoids obstacles, and detects high-priority cleaning zones (red carpets).
It demonstrates **sensor fusion**, **reactive control**, **vision-based behavior switching**, and **real-time visualization**.

---

## 🎯 Objectives

* Implement a **hybrid perception system** combining infrared sensors and a camera.
* Develop **behavior-based control** using a finite-state machine (FSM).
* Design a real-time **dashboard** showing trajectory, status, and sensor feedback.
* Evaluate robustness under different lighting, obstacles, and failure scenarios.

---

# 🏗️ System Architecture

Below is the high-level system architecture (Mermaid diagram):

```mermaid
flowchart TB
    subgraph Frontend["React Dashboard"]
        A1["RoomCanvas (Trajectory Visualizer)"]
        A2["StatusPanel (Mode, Sensors)"]
        A3["ControlPanel (User Commands)"]
    end

    subgraph Backend["FastAPI WebSocket Server"]
        B1["/ws WebSocket Endpoint"]
        B2["Broadcast Manager"]
        B3["Data Logger"]
    end

    subgraph Webots["Webots Simulation Environment"]
        C1["e-puck Robot Model"]
        C2["Python Controller"]
        C3["Infrared Sensors"]
        C4["Camera (RGB → HSV)"]
        C5["Finite State Machine"]
        C6["Motors Control"]
    end

    Frontend <--> |"WebSocket JSON Stream"| Backend
    Backend <--> |"State Updates / Commands"| Webots
    C2 --> C3
    C2 --> C4
    C2 --> C5
    C2 --> C6
```

---

# 🔄 Data Flow Diagram

```mermaid
sequenceDiagram
    participant W as Webots Controller
    participant S as FastAPI Server
    participant F as React Frontend

    W->>S: Send robot state JSON<br/>{x, y, mode, IR[], detected }
    S->>F: Broadcast live state update
    F->>F: Update UI (Canvas + Panels)

    F->>S: User command (start/pause/reset)
    S->>W: Forward command to controller

    Note over W: Robot updates state<br/>via sensors + FSM
```

---

# 🤖 Robot Behaviour (Finite State Machine)

```mermaid
stateDiagram-v2
    [*] --> Idle

    Idle --> Cleaning: Start Command
    Cleaning --> Cleaning: Normal operation
    Cleaning --> Avoiding: Obstacle detected
    Cleaning --> FocusedCleaning: Red zone detected

    Avoiding --> Cleaning: Path cleared
    FocusedCleaning --> Cleaning: Timer expired

    Cleaning --> Idle: Pause Command
    FocusedCleaning --> Idle: Pause Command
```

---

# 🖥️ Dashboard UI Layout

```mermaid
flowchart LR
    subgraph Dashboard["React Dashboard Layout"]
        direction TB
        UI1["Header: Indoor Cleaning Robot"]
        UI2["RoomCanvas (Robot Trajectory)"]
        UI3["StatusPanel (Mode / Position / Sensors)"]
        UI4["ControlPanel (Start / Pause / Reset)"]
    end
    UI1 --> UI2 --> UI3 --> UI4
```

---

## 📦 Project Structure

```
indoor-cleaning-robot/
├── webots_controller/
│   ├── cleaner_controller.py
│   ├── sensors.py
│   ├── vision.py
│   ├── motors.py
│   ├── state_machine.py
│   └── utils.py
│
├── backend/
│   ├── app.py
│   ├── websocket_manager.py
│   └── data_logger.py
│
├── frontend/
│   ├── src/
│   ├── vite.config.js
│   └── package.json
│
└── docs/
    ├── report.pdf
    └── design_diagram.png (optional)
```

---

## 🧮 Core Features

* **Obstacle Avoidance**
  Reactive control using infrared proximity sensors.

* **Red Zone Detection**
  HSV-based color segmentation to detect “dirty zones”.

* **Focused Cleaning Mode**
  Robot pauses and cleans when inside the detected red area.

* **Real-time Visualization**
  React dashboard displays trajectory, robot mode, and sensor values.

* **Experiment Logging**
  Data recorded for analysis (coverage, collisions, false detections, etc.).

---

## 🧪 Running the Project

### 1. Start Backend

```bash
cd backend
uvicorn app:app --reload
```

### 2. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3. Run Simulation in Webots

* Load world file
* Assign controller: `cleaner_controller.py`
* Run simulation

---

## 🔬 Experimental Evaluation

Experiments include:

| Experiment         | Description           | Metrics                |
| ------------------ | --------------------- | ---------------------- |
| Navigation Test    | Obstacle handling     | Collisions, smoothness |
| Red Zone Detection | Lighting variations   | Detection accuracy     |
| Focused Cleaning   | Behaviour transitions | Response time          |
| Robustness         | Random obstacles      | Stability              |

Full details are in `docs/report.pdf`.

---

## ⚠️ Limitations

* No global path planner (purely reactive).
* Color detection sensitive to illumination.
* Narrow sensor angle may miss thin obstacles.
* Occasional false positives at red edges.

---

## 📁 Repository Notes

* Robot model used: **e-puck** (Cyberbotics)
* Core logic implemented by the project team
* Standard libraries only; no pre-built navigation packages

---

## 🔗 Deliverables

* Report (IEEE format, 6 pages max)
* 5-minute demo video
* Public GitHub repository (this repo)

---

## 📜 License

MIT License – for academic and research use.
