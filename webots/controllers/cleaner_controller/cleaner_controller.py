from controller import Robot
from sensors import IRSensors
from vision import Vision
from motors import Motors
from state_machine import RobotState

class CleanerBot:
    def __init__(self):
        self.robot = Robot()
        self.ir = IRSensors(self.robot)
        self.vision = Vision(self.robot)
        self.motors = Motors(self.robot)
        self.state = RobotState.CLEANING

    def run(self):
        timestep = int(self.robot.getBasicTimeStep())
        while self.robot.step(timestep) != -1:

            if self.vision.detects_red():
                self.state = RobotState.FOCUS
            else:
                self.state = RobotState.CLEANING

            if self.state == RobotState.CLEANING:
                if self.ir.obstacle_detected():
                    self.motors.turn_left()
                else:
                    self.motors.forward()

            elif self.state == RobotState.FOCUS:
                self.motors.stop()

if __name__ == '__main__':
    CleanerBot().run()
