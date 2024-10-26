# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       ADMIN                                                        #
# 	Created:      10/26/2024, 8:09:18 PM                                       #
# 	Description:  Optimized V5 project                                         #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()

# Use a set for faster lookups and to avoid iteration issues when deleting buttons
buttonlist = set()

class Button:
    def __init__(self, x, y, width, height, label="Button", color=Color.GREEN, callback=None, enable_hold=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.color = color
        self.callback = callback
        self.enable_hold = enable_hold
        self.is_pressed_now = False

        self.draw()

        buttonlist.add(self)

    def draw(self):
        """Draw the button on the screen with centered text."""
        brain.screen.set_fill_color(self.color)
        brain.screen.set_pen_color(self.color)
        brain.screen.draw_rectangle(self.x, self.y, self.width, self.height)

        text_width = len(self.label) * 6
        text_x = self.x + (self.width - text_width) // 2 - 4
        text_y = self.y + (self.height - 8) // 2  # Center text vertically

        brain.screen.set_pen_color(Color.BLACK)
        brain.screen.print_at(self.label, x=text_x, y=text_y)

    def is_pressed(self, touch_x, touch_y):
        """Check if the button is pressed based on touch coordinates."""
        return self.x <= touch_x <= self.x + self.width and \
               self.y <= touch_y <= self.y + self.height

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
        """Remove the button visually and from the listener."""
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.set_pen_color(Color.BLACK)
        brain.screen.draw_rectangle(self.x, self.y, self.width, self.height)

        buttonlist.discard(self)

def checkforbuttons():
    """Continuously poll for button presses."""
    while True:
        if brain.screen.pressing():
            touch_x, touch_y = brain.screen.x_position(), brain.screen.y_position()

            pressed_buttons = [btn for btn in buttonlist if btn.is_pressed(touch_x, touch_y)]
            for button in pressed_buttons:
                button.handle_press()
        else:
            for button in buttonlist:
                button.reset()

        wait(0.05, SECONDS)

Thread(checkforbuttons)
