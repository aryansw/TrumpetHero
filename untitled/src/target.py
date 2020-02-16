import sys

from src.lib import Leap

sys.path.insert(0, "../lib")
import midi
import pygame

pygame.init()
pattern = midi.read_midifile("music/bohemian.mid")

# temporary code
tracks = midi.Pattern()

trackCounter = 0
for track in pattern:
    if trackCounter != 3:
        tracks.append(track)
    trackCounter = trackCounter + 1

    tracks.append(track)

    if trackCounter == 5:  # change this number to find different instruments/vocals
        i = 0
        # print(tracks[trackCounter])

    trackCounter = trackCounter + 1

if isinstance(tracks[0][0], midi.events.TrackNameEvent):
    print("It is the same")


trackNum = 3
for sub in tracks[trackNum]:
    if isinstance(sub, midi.events.NoteOnEvent) or isinstance(sub, midi.events.TrackNameEvent) or isinstance(sub, midi.events.TextMetaEvent):
        print(sub)
        print(sub.tick)

# end of temporary code
trumpet = pattern[3]
pattern.remove(trumpet)
midi.write_midifile("backingsong.mid", pattern)

pygame.mixer.music.load("backingsong.mid")
pygame.mixer.music.play()

controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
controller.set_policy(Leap.Controller.POLICY_IMAGES)
controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)


pygame.mixer.music.load("369646.mid")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)