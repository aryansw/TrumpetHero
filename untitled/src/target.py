import sys
from lib import Leap

sys.path.insert(0, "../lib")
import midi
import pygame

pygame.init()

pattern = midi.read_midifile("music/bohemian.mid")
pattern.make_ticks_abs()

# temporary code
tracks = midi.Pattern()

#trackCounter = 0
#trackNum = 0
#flag = 1
#for track in pattern:
 #   for sub in track:
 #       if isinstance(sub, midi.events.TextMetaEvent):
 #           print(sub)
 #           instrument = sub.__getattribute__("text")
 #           print(instrument)
 #           if instrument == 'Piano':
 #               trackNum = trackCounter
 #               flag = 0
 #               break
 #   if flag == 0:
 #       break
 #   trackCounter = trackCounter + 1

#if isinstance(tracks[0][0], midi.events.TrackNameEvent):
#    print("It is the same")

prev_sub_tick = 0

trackNum = 5
for sub in tracks[trackNum]:
    if isinstance(sub, midi.events.NoteOnEvent) or isinstance(sub, midi.events.TrackNameEvent) or isinstance(sub, midi.events.TextMetaEvent):
        if sub.tick > 0:
            dif = sub.tick - prev_sub_tick
            prev_sub_tick = sub.tick
            if dif > 0:
                print(sub)
                print(dif)


# end of temporary code


controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
controller.set_policy(Leap.Controller.POLICY_IMAGES)
controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)


# pygame.mixer.music.load("369646.mid")
# pygame.mixer.music.play()

# while pygame.mixer.music.get_busy():
#    pygame.time.wait(1000)

trumpet = pattern[trackNum]
pattern.remove(trumpet)
midi.write_midifile("backingsong.mid", pattern)

pygame.mixer.music.load("backingsong.mid")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)
