import sys
import midi
import pygame

import Note

pygame.init()

pattern = midi.read_midifile("music/bohemian.mid")
pattern.make_ticks_abs()

bpms = []

for sub in pattern[0]:
    if isinstance(sub, midi.events.SetTempoEvent):
        bpm = Note.bpm()
        bpm.bp = sub.get_bpm()
        bpm.ticks = sub.tick
        bpms.append(bpm)

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

prev_sub_tick = 0

total_ticks = 0
for sub in pattern[trackNum]:
    if isinstance(sub, midi.events.NoteOnEvent) or isinstance(sub, midi.events.NoteOffEvent):
        print(sub)
        total_ticks = sub

pattern.make_ticks_rel()
trumpet = pattern[trackNum]
pattern.remove(trumpet)
trumpet.make_ticks_rel()
notes = []

for event in trumpet:
    if isinstance(event, midi.events.NoteOnEvent):
        note = Note.Tune(event.pitch, event.velocity, event.tick, True)
        notes.append(note)
    if isinstance(event, midi.events.NoteOffEvent):
        note = Note.Tune(event.pitch, 0, event.tick, False)
        notes.append(note)

# CREATING NEW MIDI FILE

new_trumpet = midi.Pattern()
track = midi.Track()
new_trumpet.append(track)
new_trumpet.make_ticks_abs()
for bpm in bpms:
    tempo_event = midi.events.SetTempoEvent()
    tempo_event.set_bpm(bpm.bp)
    tempo_event.tick = bpm.ticks
    track.append(tempo_event)
new_trumpet.make_ticks_rel()
for note in notes:
    if note.canPlay:
        on = midi.NoteOnEvent()
        on.tick = note.duration
        on.pitch = note.pitch
        on.velocity = note.velocity
        track.append(on)
    if not note.canPlay:
        off = midi.NoteOffEvent()
        off.tick = note.duration
        off.pitch = note.pitch
        track.append(off)

eot = midi.EndOfTrackEvent(tick=1)
track.append(eot)

midi.write_midifile("demo1.mid", new_trumpet)

pygame.mixer.music.load("demo1.mid")
pygame.mixer.music.play()

print("here")
while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)
""""
midi.write_midifile("backingsong.mid", pattern)

pygame.mixer.music.load("backingsong.mid")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
   pygame.time.wait(1000)
"""
