import sys
sys.path.insert(0, "../lib")
import midi
import pygame

pygame.init()
pattern = midi.read_midifile("music/bohemian.mid")

# temporary code
tracks = midi.Pattern()

trackCounter = 0
trackNum = 0
flag = 1
for track in pattern:
    for sub in track:
        if isinstance(sub, midi.events.TextMetaEvent):
            print(sub)
            instrument = sub.__getattribute__("text")
            print(instrument)
            if instrument == 'Piano':
                trackNum = trackCounter
                flag = 0
                break
    if flag == 0:
        break
    trackCounter = trackCounter + 1

trumpet = pattern[trackNum]
pattern.remove(trumpet)
midi.write_midifile("backingsong.mid", pattern)

pygame.mixer.music.load("backingsong.mid")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)