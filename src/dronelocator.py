import threading
from time import sleep
import math


# The DroneLocator class is designed to simulate the movement and tracking of a
# drone's position on a 2D plane.
class DroneLocator:
    interval = 0.25  # Interval in seconds for updates
    # Distance and rotation per interval
    # Different values than in Config, due to accuracy issues. (more in documentation)
    move_speed = 25 * interval
    rotation_speed = 72 * interval
    x, y = 350, 350  # Initial x, y coordinates on the map
    accumulated_angle = 0
    points = [(0, 0), (0, 0)]  # Where the drone has been

    # Stores the current speed for each axis and rotation, privately for DroneLocator
    axis_speed = {"rotation": 0, "right-left": 0, "forward-back": 0, "up-down": 0}

    # The watch method starts a new thread that continuously updates the drone's position
    def watch(self):
        # Nested function
        # Calls update() every interval
        def draw_map(locator: DroneLocator):
            while True:
                locator.update()
                sleep(DroneLocator.interval)

        # Starting new thread for draw_map()
        td = threading.Thread(target=draw_map, args=(self,))
        td.start()

    # Updates the axis_speed every time after new command is sent to Drone
    def update_axis(self, right_left, forward_back, up_down, rotation):
        self.axis_speed = {
            "rotation": rotation,
            "right-left": right_left,
            "forward-back": forward_back,
            "up-down": up_down
        }

    # Append the current position to the points list if it has
    # changed since the last update.
    def update(self):
        self.calculate_current_position()
        if self.points[-1][0] != self.x or self.points[-1][1] != self.y:
            self.points.append((self.x, self.y))

    # Calculates the drone's position and updates the x, y coordinates.
    def calculate_current_position(self):
        distance = 0
        direction = 0

        # Calculate the distance and direction based on the axis_speed values.
        # Negative values for right-left indicate left movement, positive indicate right.
        if self.axis_speed["right-left"] < 0:
            distance = self.move_speed
            direction = -90
        elif self.axis_speed["right-left"] > 0:
            distance = self.move_speed
            direction = 90

        # Negative values for forward-back indicate backward movement, positive indicate forward.
        if self.axis_speed["forward-back"] > 0:
            distance = self.move_speed
            direction = 0
        elif self.axis_speed["forward-back"] < 0:
            distance = self.move_speed
            direction = 180

        # Update the accumulated_angle based on the rotation speed.
        # Negative values for rotation indicate left rotation, positive indicate right.
        if self.axis_speed["rotation"] < 0:
            self.accumulated_angle -= self.rotation_speed
        elif self.axis_speed["rotation"] > 0:
            self.accumulated_angle += self.rotation_speed

        # Calculate the final angle by adding the direction to the accumulated angle.
        angle = direction + self.accumulated_angle

        # Update the x, y coordinates based on the calculated distance and angle.
        self.x += int(distance * math.cos(math.radians(angle)))
        self.y += int(distance * math.sin(math.radians(angle)))
