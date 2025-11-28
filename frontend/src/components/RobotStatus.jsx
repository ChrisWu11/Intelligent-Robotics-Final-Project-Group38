export default function RobotStatus({ state, cleanedZones }) {
  return (
    <div style={{ padding: 20 }}>
      <h2>Robot Status</h2>
      <p><strong>Mode:</strong> {state}</p>

      <h3>Cleaned Areas:</h3>
      <ul>
        {cleanedZones.map((z) => (
          <li key={z}>Zone {z}</li>
        ))}
      </ul>
    </div>
  );
}
