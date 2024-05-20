from djitellopy import tello as tello
from src.dronelocator import DroneLocator


# The Drone class is a high-level abstraction for controlling a Tello drone
class Drone:
    is_flying = False  # Flag to indicate if the drone is currently flying

    def __init__(self):
        self.sdk = tello.Tello()  # Initialize the Tello SDK
        self.drone_locator = DroneLocator()  # Create a DroneLocator instance
        self.drone_locator.watch()  # Start tracking the drone's position
        self.start_stream()  # Start video streaming

    # Connect to the drone using the SDK
    def start(self):
        self.sdk.connect()

    # Get the current battery level of the drone
    def get_battery(self):
        return self.sdk.get_battery()

    # Retrieve the current video frame from the drone's camera
    def get_frame(self):
        return self.sdk.get_frame_read().frame

    # Start video streaming from the drone's camera
    def start_stream(self):
        self.sdk.streamon()

    # Take off the drone and set the is_flying flag to True
    def takeoff(self):
        self.is_flying = True
        self.sdk.takeoff()

    # Land the drone and set the is_flying flag to False
    def land(self):
        self.is_flying = False
        self.sdk.land()

    # Send an emergency signal to the drone to stop all motors immediately
    def emergency(self):
        self.is_flying = False
        self.sdk.emergency()

    # Update the drone's movement along the axes and rotation.
    def update(self, right_left, forward_back, up_down, rotation):
        # Update the DroneLocator
        self.drone_locator.update_axis(right_left, forward_back, up_down, rotation)
        # Send the control signals to the drone
        self.sdk.send_rc_control(right_left, forward_back, up_down, rotation)

    # Retrieve the history of positions that the drone has been in
    def get_position_history(self):
        return self.drone_locator.points

    # Reset the position history to the initial point
    def clean_position_history(self):
        self.drone_locator.points = [(0, 0)]
