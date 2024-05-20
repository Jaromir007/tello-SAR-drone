import cv2
from src.drone import Drone
from src.pygamescreen import PygameScreen


# Responsible for controlling all actions
class TelloEngine(object):

    # Initialize the TelloEngine with a Drone object.
    def __init__(self, drone: Drone):
        self.drone = drone
        # Current speed
        self.axis_speed = {"rotation": 0, "right-left": 0, "forward-back": 0, "up-down": 0}
        # Commanded speed
        self.cmd_axis_speed = {"rotation": 0, "right-left": 0, "forward-back": 0, "up-down": 0}
        # Copy of the axis_speed to track changes
        self.prev_axis_speed = self.axis_speed.copy()
        self.battery = self.drone.get_battery()
        # Initialize the PygameScreen with key event listeners
        self.pygame_screen = PygameScreen(self)
        self.pygame_screen.add_listeners()

    # Set the commanded speed for a given axis.
    def set_speed(self, axis, speed):
        self.cmd_axis_speed[axis] = speed

    # Process the current frame, update the drone's speed, and send commands.
    def process(self):
        self.axis_speed = self.cmd_axis_speed.copy()
        self.show_frame()
        self.send_drone_command()

    # Display the current frame from the drone's camera
    def show_frame(self):
        img = self.drone.get_frame()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # reverse mirror effect
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (1280, 720))
        cv2.imshow("Drone stream", img)

    # Send the updated speed commands to the drone if there are changes.
    def send_drone_command(self):
        # Check for changes
        for axis, speed in self.axis_speed.items():
            if self.axis_speed[axis] != self.prev_axis_speed[axis]:
                self.prev_axis_speed[axis] = self.axis_speed[axis]

        # Send the control signals to the drone.
        self.drone.update(
            int(self.axis_speed["right-left"]),
            int(self.axis_speed["forward-back"]),
            int(self.axis_speed["up-down"]),
            int(self.axis_speed["rotation"])
        )
