import sys

sys.path.insert(0, "../lib")
import midi
import pygame

pygame.init()

pattern = midi.read_midifile("../BohemianRhapsody.mid")

# temporary code
tracks = []

trackCounter = 0
for track in pattern:
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


controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
controller.set_policy(Leap.Controller.POLICY_IMAGES)
controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)


#pygame.mixer.music.load("369646.mid")
#pygame.mixer.music.play()

#while pygame.mixer.music.get_busy():
#    pygame.time.wait(1000)