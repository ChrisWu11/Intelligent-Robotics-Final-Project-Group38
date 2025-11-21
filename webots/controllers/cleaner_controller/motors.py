class Motors:
    def __init__(self, robot):
        self.left = robot.getDevice('left wheel motor')
        self.right = robot.getDevice('right wheel motor')
        self.left.setPosition(float('inf'))
        self.right.setPosition(float('inf'))

    def forward(self):
        self.left.setVelocity(4)
        self.right.setVelocity(4)

    def turn_left(self):
        self.left.setVelocity(-4)
        self.right.setVelocity(4)

    def stop(self):
        self.left.setVelocity(0)
        self.right.setVelocity(0)
