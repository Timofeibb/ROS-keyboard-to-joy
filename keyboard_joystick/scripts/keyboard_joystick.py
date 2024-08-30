#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Joy
import sys
import select
import termios
import tty

# Key mappings
KEY_MAPPING = {
    'w': [0, -1], 'a': [-1, 0], 's': [0, 1], 'd': [1, 0],  # Left stick (WASD)
    'i': [1, 0], 'j': [0, 1], 'k': [-1, 0], 'l': [0, -1],  # Right stick (IJKL)
}

class KeyboardJoystick:
    def __init__(self):
        self.pub = rospy.Publisher('/joy', Joy, queue_size=10)
        self.left_stick = [0, 0]  # Initialize left stick [x, y]
        self.right_stick = [0, 0]  # Initialize right stick [x, y]
        self.buttons = [0] * 12  # Initialize 12 buttons (all set to 0)
        self.old_attr = termios.tcgetattr(sys.stdin)
        
        # Print usage information
        self.print_usage()

    def print_usage(self):
        usage_msg = """
        Keyboard Joystick Node

        Use the following keys to control the joystick:

        Left Stick:
        W - Forward
        S - Backward
        A - Left
        D - Right

        Right Stick:
        I - Forward
        K - Backward
        J - Left
        L - Right

        Press ESC to exit the node.

        """
        print(usage_msg)

    def get_key(self):
        tty.setraw(sys.stdin.fileno())  # Switch to raw mode (no buffering, no echo)
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_attr)  # Restore settings
        return key

    def run(self):
        rate = rospy.Rate(10)  # 10 Hz
        while not rospy.is_shutdown():
            key = self.get_key()
            if key == '\x1b':  # ESC key to exit
                rospy.signal_shutdown("User requested shutdown.")
                break
            if key in KEY_MAPPING:
                if key in 'wasd':
                    self.left_stick = KEY_MAPPING[key]
                elif key in 'ijkl':
                    self.right_stick = KEY_MAPPING[key]
            else:
                self.left_stick = [0, 0]
                self.right_stick = [0, 0]

            # Create and publish Joy message
            joy_msg = Joy()
            joy_msg.axes = self.left_stick + self.right_stick
            joy_msg.buttons = self.buttons
            self.pub.publish(joy_msg)
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('keyboard_joystick')
    kj = KeyboardJoystick()
    try:
        kj.run()
    except rospy.ROSInterruptException:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, kj.old_attr)  # Ensure terminal settings are restored