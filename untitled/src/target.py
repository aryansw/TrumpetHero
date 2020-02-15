import sys
sys.path.insert(0, "../lib")
import midi
from lib import Leap

pattern = midi.read_midifile("../369646.mid")


# temporary code
tracks = []

trackCounter = 0
for track in pattern:
    tracks.append(track)

    if trackCounter == 5:  # change this number to find different instruments/vocals
        print(tracks[trackCounter])

    trackCounter = trackCounter + 1


if isinstance(tracks[0][0], midi.events.TrackNameEvent):
    print("It is the same")

# end of temporary code

controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
controller.set_policy(Leap.Controller.POLICY_IMAGES)
controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)


print("Hello")
