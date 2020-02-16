import sys
from lib import Leap

from midi2audio import FluidSynth

sys.path.insert(0, "../lib")
import midi
import pygame

pygame.init()


pattern = midi.read_midifile("music/bohemian.mid")
pattern.make_ticks_abs()



# temporary code
tracks = pattern

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

trackNum = 0
for sub in tracks[trackNum]:
    # if isinstance(sub, midi.events.NoteOnEvent) or isinstance(sub, midi.events.TrackNameEvent) or isinstance(sub, midi.events.TextMetaEvent) or isinstance(sub, midi.events.SetTempoEvent):
      #   if sub.tick > 0:
          #  dif = sub.tick - prev_sub_tick
         #   prev_sub_tick = sub.tick
        #    if dif > 0:
    if isinstance(sub, midi.events.SetTempoEvent):
        print(sub)
        print(60000 / ((sub.get_mpqn() / 1000) * sub.get_bpm()))
        print(sub.get_mpqn())
        print(sub.get_bpm())
        print('\n')
         #       print(dif)


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

#pygame.mixer.init()
# Load two sounds
#snd1 = pygame.mixer.Sound('music/369646.mid')
#snd2 = pygame.mixer.Sound('music/bohemian.mid')
# Play the sounds; these will play simultaneously
#snd1.play()
#snd2.play()

pygame.mixer.music.load("music/369646.mid")
pygame.mixer.music.load("music/bohemian.mid")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)
