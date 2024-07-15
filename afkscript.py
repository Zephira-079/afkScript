from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
import time
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Load the image and convert to numpy format
ImageAddress = "./icon/IAmAFK-png.png"
ImageItself = Image.open(ImageAddress)
ImageNumpyFormat = np.asarray(ImageItself)

# Get the countdown time from the user, default to 120 seconds if not provided
try:
    countdown = int(input("Seconds before considering AFK: ")) or 120
except ValueError:
    countdown = 120 

t_countdown = 0

mouse = MouseController()
keyboard = KeyboardController()

# Get initial mouse position
x, y = mouse.position

# Set up matplotlib for interactive mode
plt.ion()

while True:
    c_x, c_y = mouse.position

    if c_x != x or c_y != y:
        # Mouse is moving
        print("Mouse is moving")
        x = c_x
        y = c_y
        t_countdown = 0  # Reset countdown
        
        # Close the AFK image if it's open
        plt.close()
        
    else:
        # Mouse is not moving
        if t_countdown == countdown:
            # Display the AFK image
            plt.imshow(ImageNumpyFormat)
            plt.draw()
            plt.pause(0.01)  # Small pause to ensure the image updates
            t_countdown += 1
        else:
            t_countdown += 1
        
        print(f"Countdown: {t_countdown}/{countdown} seconds")

    time.sleep(1)
