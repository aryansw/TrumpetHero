import sys
from lib import Leap

sys.path.insert(0, "../lib")
import midi
import pygame

import Note

pygame.init()

pattern = midi.read_midifile("music/bohemian.mid")
# pattern = midi.read_midifile("demo1.mid")
# pattern = midi.read_midifile("music/369646.mid")
pattern.make_ticks_rel()

bpms = []

timeSigCounter = 0

for sub in pattern[0]:
    if isinstance(sub, midi.events.SetTempoEvent):
        bpm = Note.bpm()
        bpm.bp = sub.get_bpm()
        print(bpm.bp)
        print(sub.get_mpqn())
        bpm.ticks = sub.tick
        bpms.append(bpm)
    elif isinstance(sub, midi.events.TimeSignatureEvent):
        bpms[timeSigCounter].bp = bpms[timeSigCounter].bp * (sub.data[0] / sub.data[1])
        print(sub.numerator)
        print(sub.denominator)
        print(bpms[timeSigCounter].bp)

tracks = pattern

trackCounter = 0
trackNum = 0
flag = 1
for track in pattern:
    for sub in track:
        print(sub)
        if isinstance(sub, midi.events.TextMetaEvent) or isinstance(sub, midi.events.TrackNameEvent):
            # print(sub)
            instrument = sub.__getattribute__("text")
            print(instrument)
            if instrument == 'Piano':
                trackNum = trackCounter
                flag = 0
                break
    if flag == 0:
        break
    trackCounter = trackCounter + 1



controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
controller.set_policy(Leap.Controller.POLICY_IMAGES)
controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)

total_ticks = 0
for sub in pattern[trackNum]:
    if isinstance(sub, midi.events.NoteOnEvent) or isinstance(sub, midi.events.NoteOffEvent):
        print(sub)
        total_ticks = sub.tick

# pattern.make_ticks_rel()
trumpet = pattern[trackNum]
pattern.remove(trumpet)
# trumpet.make_ticks_rel()
notes = []

prevTick = 0

for event in trumpet:
    if isinstance(event, midi.events.NoteOnEvent):
        note = Note.Tune(event.pitch, event.velocity, event.tick, True)
        notes.append(note)
        prevTick = event.tick
        # print(prevTick)
    elif isinstance(event, midi.events.NoteOffEvent):
        note = Note.Tune(event.pitch, 0, event.tick, False)
        notes.append(note)
        prevTick = event.tick
        # print(prevTick)

# CREATING NEW MIDI FILE

new_trumpet = midi.Pattern()
track = midi.Track()
track.make_ticks_rel()
new_trumpet.append(track)
new_trumpet.make_ticks_rel()


for bpm in bpms:
    tempo_event = midi.events.SetTempoEvent()
    tempo_event.set_bpm(bpm.bp)
    #tempo_event..tick = bpm.ticks
    track.append(tempo_event)
# new_trumpet.make_ticks_rel()

#time_event = og_time_event
#track.append(time_event)


tot_ticks = 0  # notes[0].duration
for note in notes:
    if note.canPlay:
        on = midi.NoteOnEvent()
        on.tick = note.duration
        print(on.tick)
        on.pitch = note.pitch
        on.velocity = note.velocity
        track.append(on)
        tot_ticks = tot_ticks + on.tick
    if not note.canPlay:
        off = midi.NoteOffEvent()
        off.tick = note.duration
        print(off.tick)
        off.pitch = note.pitch
        track.append(off)
        tot_ticks = tot_ticks + off.tick

eot = midi.EndOfTrackEvent(tick=1)
track.append(eot)

midi.write_midifile("demo1.mid", new_trumpet)

pygame.mixer.music.load("demo1.mid")
pygame.mixer.music.play()




print("here")
print(total_ticks)

while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)
""""
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
"""
