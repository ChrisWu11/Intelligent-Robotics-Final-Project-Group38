import { useEffect, useState } from "react";

export default function App() {
  const [path, setPath] = useState([]);

  // Webots world boundary
  const minX = -10;
  const maxX = 2;
  const minY = -7;
  const maxY = 1;

  const width = 1200;   // 展示区域宽度
  const height = 800;   // 展示区域高度

  // Convert Webots → screen
  const convert = (x, y) => {
    const screenX = ((x - minX) / (maxX - minX)) * width;
    const screenY = height - ((y - minY) / (maxY - minY)) * height;
    return { x: screenX, y: screenY };
  };

  // Room corners
  const c1 = convert(minX, minY);
  const c2 = convert(maxX, minY);
  const c3 = convert(maxX, maxY);
  const c4 = convert(minX, maxY);
  const roomPolygon = `${c1.x},${c1.y} ${c2.x},${c2.y} ${c3.x},${c3.y} ${c4.x},${c4.y}`;

  // WebSocket connection
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8765/ws");

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.supervisor_x !== undefined) {
        const p = convert(msg.supervisor_x, msg.supervisor_y);
        setPath((prev) => [...prev, p]);
      }
    };

    return () => ws.close();
  }, []);

  return (
    <div style={styles.page}>
      <h1 style={styles.title}>Robot Path Visualization</h1>

      <div style={styles.canvasWrapper}>
        <svg width={width} height={height} style={styles.svg}>

          {/* Room border */}
          <polygon
            points={roomPolygon}
            fill="none"
            stroke="#666"
            strokeWidth={4}
          />

          {/* Path */}
          <polyline
            points={path.map((p) => `${p.x},${p.y}`).join(" ")}
            fill="none"
            stroke="#3ec6ff"
            strokeWidth={3}
          />
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
    justifyContent: "flex-start",
    paddingTop: "40px",
    fontFamily: "'Inter', sans-serif",
  },

  title: {
    fontSize: "32px",
    fontWeight: "700",
    marginBottom: "20px",
    color: "#333",
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
