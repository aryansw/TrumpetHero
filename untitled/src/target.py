import sys
sys.path.insert(0, "../lib")
import midi
from lib import Leap

pattern = midi.read_midifile("369646.mid")
print(pattern)

controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
controller.set_policy(Leap.Controller.POLICY_IMAGES)
controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)


print("Hello")