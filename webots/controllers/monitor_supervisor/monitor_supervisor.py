from controller import Supervisor

robot = Supervisor()
TIME_STEP = int(robot.getBasicTimeStep())

epuck = robot.getFromDef("CLEANER")
trans = epuck.getField("translation")
rot = epuck.getField("rotation")

while robot.step(TIME_STEP) != -1:
    print("Position:", trans.getSFVec3f())
    print("Rotation:", rot.getSFRotation())
