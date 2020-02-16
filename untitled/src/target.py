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

# end of temporary code
trumpet = pattern[3]
pattern.remove(trumpet)
midi.write_midifile("backingsong.mid", pattern)

pygame.mixer.music.load("backingsong.mid")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)
print("Hello")