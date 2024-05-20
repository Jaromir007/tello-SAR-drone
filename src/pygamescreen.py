import time
import pygame
from src.config import Config


# The PygameScreen class is responsible for handling keyboard events to control a drone.
class PygameScreen:

    # Initialize the Pygame window and set up key event listeners.
    def __init__(self, engine):
        self.controls_keypress, self.controls_keyrelease = get_keys_control(engine)
        self.screen = self.init_pygame_screen()
        self.listeners = {}
        self.running = True

    # Initialize the Pygame screen.
    @staticmethod
    def init_pygame_screen():
        pygame.init()
        # Set the window size and fill it with a white background.
        screen = pygame.display.set_mode([420, 700])
        screen.fill((255, 255, 255))
        return screen

    # Add an event listener function
    def add_listener(self, fn, event):
        self.listeners[event] = fn

    # Check for Pygame events and call the corresponding functions.
    def watch_events(self):
        for event in pygame.event.get():
            if event.type in self.listeners:
                self.listeners[event.type](event)

    # Add the key press and release listeners
    def add_listeners(self):
        self.add_listener(self.keypress_listener, pygame.KEYDOWN)
        self.add_listener(self.keyrelease_listener, pygame.KEYUP)

    # Listener for key press events
    def keypress_listener(self, event):
        if event.key in self.controls_keypress:
            self.controls_keypress[event.key]()

    # Listener for key release
    def keyrelease_listener(self, event):
        if event.key in self.controls_keyrelease:
            self.controls_keyrelease[event.key]()


# Function to map keyboard keys to drone control functions.
def get_keys_control(engine):
    # Key released:
    controls_key_release = {
        pygame.K_w: lambda: engine.set_speed("up-down", 0),
        pygame.K_s: lambda: engine.set_speed("up-down", 0),
        pygame.K_a: lambda: engine.set_speed("rotation", 0),
        pygame.K_d: lambda: engine.set_speed("rotation", 0),
        pygame.K_LEFT: lambda: engine.set_speed("right-left", 0),
        pygame.K_RIGHT: lambda: engine.set_speed("right-left", 0),
        pygame.K_UP: lambda: engine.set_speed("forward-back", 0),
        pygame.K_DOWN: lambda: engine.set_speed("forward-back", 0)
    }

    # Key pressed:
    controls_key_press = {
        pygame.K_w: lambda: engine.set_speed("up-down", Config.def_speed["up-down"]),
        pygame.K_s: lambda: engine.set_speed("up-down", -Config.def_speed["up-down"]),
        pygame.K_a: lambda: engine.set_speed("rotation", -Config.def_speed["rotation"]),
        pygame.K_d: lambda: engine.set_speed("rotation", Config.def_speed["rotation"]),
        pygame.K_LEFT: lambda: engine.set_speed("right-left", -Config.def_speed["right-left"]),
        pygame.K_RIGHT: lambda: engine.set_speed("right-left", Config.def_speed["right-left"]),
        pygame.K_UP: lambda: engine.set_speed("forward-back", Config.def_speed["forward-back"]),
        pygame.K_DOWN: lambda: engine.set_speed("forward-back", -Config.def_speed["forward-back"]),
        pygame.K_TAB: lambda: engine.drone.takeoff(),
        pygame.K_BACKSPACE: lambda: engine.drone.land(),
        pygame.K_e: lambda: engine.drone.emergency()
    }
    return controls_key_press, controls_key_release
