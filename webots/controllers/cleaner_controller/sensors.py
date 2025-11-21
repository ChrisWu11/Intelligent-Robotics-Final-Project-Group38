class IRSensors:
    def __init__(self, robot):
        self.sensors = []
        for i in range(8):
            s = robot.getDevice(f'ps{i}')
            s.enable(64)
            self.sensors.append(s)

    def get_values(self):
        return [s.getValue() for s in self.sensors]

    def obstacle_detected(self):
        values = self.get_values()
        return values[0] > 80 or values[7] > 80
