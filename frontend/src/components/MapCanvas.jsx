import { useEffect, useRef } from "react";

export default function MapCanvas({ trajectory, cleanedZones }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    // Clear
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw red/green zones
    cleanedZones.forEach((id) => {
      // 假设 id 是 "zone1", "zone2"... 你可以加上坐标映射
      const x = 50 + id * 30;
      const y = 50;

      ctx.fillStyle = "green";
      ctx.fillRect(x, y, 20, 20);
    });

    // Draw robot trajectory
    ctx.strokeStyle = "blue";
    ctx.lineWidth = 2;
    ctx.beginPath();

    trajectory.forEach((p, idx) => {
      const scale = 40;  // 缩放系数，可调整
      const x = canvas.width / 2 + p.x * scale;
      const y = canvas.height / 2 - p.y * scale;

      if (idx === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });

    ctx.stroke();
  }, [trajectory, cleanedZones]);

  return (
    <canvas
      ref={canvasRef}
      width={600}
      height={400}
      style={{ border: "1px solid black", marginRight: 20 }}
    />
  );
}
