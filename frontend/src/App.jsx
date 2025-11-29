import { useEffect, useState } from "react";

export default function App() {
  const [path, setPath] = useState([]);
  const [cleaned, setCleaned] = useState([]);
  const [robotState, setRobotState] = useState("EXPLORE");
  const [robot, setRobot] = useState({ x: 0, y: 0, ry: 0 });

  // Webots world boundaries
  const minX = -10;
  const maxX = 2;
  const minY = -7;
  const maxY = 1;

  const width = 1200;
  const height = 800;

  const convert = (x, y) => {
    return {
      x: ((x - minX) / (maxX - minX)) * width,
      y: height - ((y - minY) / (maxY - minY)) * height,
    };
  };

  // Room border polygon
  const c1 = convert(minX, minY);
  const c2 = convert(maxX, minY);
  const c3 = convert(maxX, maxY);
  const c4 = convert(minX, maxY);
  const roomPolygon = `${c1.x},${c1.y} ${c2.x},${c2.y} ${c3.x},${c3.y} ${c4.x},${c4.y}`;

  // WebSocket
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8765/ws");

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);

      if (msg.type === "position") {
        const p = convert(msg.x, msg.y);
        setRobot({
          x: p.x,
          y: p.y,
          ry: msg.ry, // rotation from backend
        });
        setPath((prev) => [...prev, p]);
      }

      if (msg.type === "cleaned_zone") {
        const newPoints = msg.zones.map((z) => convert(z.x, z.y));
        setCleaned(newPoints);
        setRobotState("CLEAN");
        setTimeout(() => setRobotState("EXPLORE"), 2000);
      }
    };

    return () => ws.close();
  }, []);

  // 🔺 Robot triangle (size adjustable)
  const triangle = (() => {
    const size = 18;
    const { x, y, ry } = robot;

    // triangle pointing forward
    const p1 = `${x},${y - size}`;
    const p2 = `${x - size * 0.6},${y + size * 0.8}`;
    const p3 = `${x + size * 0.6},${y + size * 0.8}`;
    const points = `${p1} ${p2} ${p3}`;

    return (
      <polygon
        points={points}
        fill="#ff5733"
        transform={`rotate(${(ry * 180) / Math.PI}, ${x}, ${y})`}
        opacity="0.9"
      />
    );
  })();

  return (
    <div style={styles.page}>
      <h1 style={styles.title}>Robot Path Visualization</h1>

      <div style={styles.stateBox}>
        State:{" "}
        <span
          style={{
            color: robotState === "CLEAN" ? "#2ecc71" : "#3498db",
            fontWeight: 700,
          }}
        >
          {robotState}
        </span>
      </div>

      <div style={styles.canvasWrapper}>
        <svg width={width} height={height} style={styles.svg}>

          {/* Room border */}
          <polygon
            points={roomPolygon}
            fill="none"
            stroke="#666"
            strokeWidth={4}
          />

          {/* Cleaned points */}
          {cleaned.map((p, idx) => (
            <circle key={idx} cx={p.x} cy={p.y} r="8" fill="#2ecc71" opacity="0.85" />
          ))}

          {/* Robot path */}
          <polyline
            points={path.map((p) => `${p.x},${p.y}`).join(" ")}
            fill="none"
            stroke="#3ec6ff"
            strokeWidth={3}
          />

          {/* 🔺 Robot orientation triangle */}
          {triangle}
        </svg>
      </div>
    </div>
  );
}

const styles = {
  page: {
    width: "100vw",
    height: "100vh",
    background: "#f2f2f7",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    paddingTop: "40px",
    fontFamily: "'Inter', sans-serif",
  },
  title: {
    fontSize: "32px",
    fontWeight: "700",
    marginBottom: "10px",
    color: "#333",
  },
  stateBox: {
    fontSize: "20px",
    marginBottom: "20px",
    background: "white",
    padding: "10px 18px",
    borderRadius: "8px",
    boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
  },
  canvasWrapper: {
    width: "1200px",
    height: "800px",
    background: "white",
    borderRadius: "12px",
    boxShadow: "0 8px 20px rgba(0,0,0,0.15)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  svg: {
    borderRadius: "12px",
  },
};
