class BehaviorFSM:
    def __init__(self):
        self.state = "EXPLORE"
        self.counter = 0

    def update(self, red_detected):
        if self.state == "EXPLORE":
            if red_detected:
                self.state = "CLEAN"
                self.counter = 20  # clean for 20 cycles
        elif self.state == "CLEAN":
            self.counter -= 1
            if self.counter <= 0:
                self.state = "EXPLORE"
