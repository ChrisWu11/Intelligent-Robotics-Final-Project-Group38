import { useEffect, useState } from "react";
import MapCanvas from "./components/MapCanvas";
import RobotStatus from "./components/RobotStatus";

export default function App() {
  const [trajectory, setTrajectory] = useState([]);
  const [robotState, setRobotState] = useState("EXPLORE");
  const [cleanedZones, setCleanedZones] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8765/ws");

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      console.log('msg',msg)

      // 1. 更新轨迹
      if (msg.x !== undefined && msg.y !== undefined) {
        setTrajectory((prev) => [...prev, { x: msg.x, y: msg.y }]);
      }

      // 2. 更新状态
      if (msg.state) {
        setRobotState(msg.state);
      }

      // 3. 更新已清洁区域
      if (msg.cleaned_zones) {
        setCleanedZones(msg.cleaned_zones);
      }
    };

    ws.onopen = () => console.log("[WS] Connected to backend");
    ws.onclose = () => console.log("[WS] Disconnected");

    return () => ws.close();
  }, []);

  return (
    <div style={{ display: "flex", padding: 20 }}>
      <MapCanvas trajectory={trajectory} cleanedZones={cleanedZones} />

      <RobotStatus state={robotState} cleanedZones={cleanedZones} />
    </div>
  );
}
