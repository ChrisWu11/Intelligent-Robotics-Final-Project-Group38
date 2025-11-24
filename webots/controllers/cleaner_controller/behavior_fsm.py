class FSM:
    def __init__(self):
        self.state = "explore"

    def update(self, red_detected):
        if self.state == "explore":
            if red_detected:
                self.state = "focused_cleaning"

        elif self.state == "focused_cleaning":
            if not red_detected:
                self.state = "explore"
