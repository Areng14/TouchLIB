# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       ADMIN                                                        #
# 	Created:      10/26/2024, 8:09:18 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()

buttonlist = []

class Button:
    def __init__(self, x, y, width, height, label="Button", color=Color.GREEN, callback=None, enable_hold=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.color = color
        self.callback = callback
        self.enable_hold = enable_hold  # Option to allow continuous pressing
        self.is_pressed_now = False  # Track if the button is pressed

    def draw(self):
        """Draw the button on the screen with centered text."""
        brain.screen.set_fill_color(self.color)
        brain.screen.set_pen_color(self.color)
        brain.screen.draw_rectangle(self.x, self.y, self.width, self.height, self.color)

        text_width = len(self.label) * 6 
        text_height = 8 

        text_x = self.x + ((self.width - text_width) // 2) - 4
        text_y = self.y + ((self.width - text_width) // 2)

        brain.screen.set_pen_color(Color.BLACK)
        brain.screen.print_at(self.label, x=text_x, y=text_y)
        # Add to button listener
        buttonlist.append(self)

    def is_pressed(self, touch_x, touch_y):
        """Check if the button is pressed based on touch coordinates."""
        return (self.x <= touch_x <= self.x + self.width and
                self.y <= touch_y <= self.y + self.height)

    def handle_press(self):
        """Trigger the callback if the button is pressed."""
        if self.enable_hold or not self.is_pressed_now:
            if self.callback:
                self.callback()
            self.is_pressed_now = True

    def reset(self):
        """Reset the button state when released."""
        self.is_pressed_now = False

    def delete(self):
        """Removes the button visually and from the listener."""
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.set_pen_color(Color.BLACK)

        brain.screen.draw_rectangle(self.x, self.y, self.width, self.height)
        if self in buttonlist:
            buttonlist.remove(self)

def checkforbuttons():
    """Continuously poll for button presses."""
    while True:
        if brain.screen.pressing():
            touch_x = brain.screen.x_position()
            touch_y = brain.screen.y_position()

            for button in buttonlist:
                if button.is_pressed(touch_x, touch_y):
                    button.handle_press()
        else:
            # Reset the state of all buttons when the screen is released
            for button in buttonlist:
                button.reset()

        wait(0.05, SECONDS)  # Prevent CPU overload

# Example usage
def say_hello():
    brain.screen.print("Hello from the Brain!")

def motor_start():
    global button2
    brain.screen.print("Deleting")
    button2.delete()

# Create buttons with and without hold behavior
button1 = Button(10, 20, 100, 50, "Greet", Color.BLUE, say_hello, enable_hold=False)
button2 = Button(120, 20, 100, 50, "Delete", Color.RED, motor_start, enable_hold=False)

# Draw buttons on the screen
button1.draw()
button2.draw()

# Start polling for button presses in a separate thread
Thread(checkforbuttons)
