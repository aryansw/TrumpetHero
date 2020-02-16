################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import sys
import midi
from lib import Leap

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def check_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        pressed = False
        indexPressed = False
        ringPressed = False
        middlePressed = False
        sawLeft = False
        # Get hands
        for hand in frame.hands:
            
            handType = "Left hand" if hand.is_left else "Right hand"
            if handType == "Left hand":
                sawLeft = True

            ringDir = 0
            middleDir = 0
            indexDir = 0

            # Get fingers
            for finger in hand.fingers:
                name = self.finger_names[finger.type]
                dir = finger.direction[1]

                if name == 'Middle':
                    middleDir = dir
                elif name == 'Ring':
                    ringDir = dir
                elif name == 'Index':
                    indexDir = dir
            
            if handType == "Left hand":
                if handType != 0 and indexDir < -0.5:
                    pressed = True

            else:
                if handType != 0 and indexDir < -0.5:
                    indexPressed = True
                
                if handType != 0 and ringDir < -0.5:
                    ringPressed = True
                
                if handType != 0 and middleDir < -0.5:
                    middlePressed = True


        return [pressed, ringPressed, middlePressed, indexPressed, sawLeft]

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
