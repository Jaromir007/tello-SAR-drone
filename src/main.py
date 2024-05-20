import cv2

from src.telloengine import TelloEngine
from src.drone import Drone


# the control loop for the drone.
def main():
    # Create and connect drone
    drone = Drone()
    drone.start()
    # Initialize the TelloEngine
    engine = TelloEngine(drone)

    # Main loop to process Pygame events and update the drone's state.
    try:
        while True:
            engine.pygame_screen.watch_events()
            engine.process()
    except KeyboardInterrupt:
        # Handle a keyboard interrupt (Ctrl+C) to ensure the drone lands.
        print("Interrupt received, shutting down...")
        drone.land()
    finally:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
