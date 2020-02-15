import sys
sys.path.insert(0, "../lib")
import midi
import pygame

pygame.init()

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

pygame.mixer.music.load("369646.mid")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)
print("Hello")