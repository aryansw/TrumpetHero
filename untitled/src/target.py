import sys
import midi
import pygame

import Note

pygame.init()

pattern = midi.read_midifile("music/bohemian.mid")

bpms = []

for sub in pattern[0]:
    if isinstance(sub, midi.events.SetTempoEvent):
        bpm = Note.bpm()
        bpm.bp = sub.get_bpm()
        bpm.ticks = sub.tick
        bpms.append(bpm)

print pattern

trackCounter = 0
trackNum = 0
flag = 1
for track in pattern:
    for sub in track:
        if isinstance(sub, midi.events.TextMetaEvent) or isinstance(sub, midi.events.TrackNameEvent):
            instrument = sub.__getattribute__("text")
            if instrument == 'Piano':
                trackNum = trackCounter
                flag = 0
                break
    if flag == 0:
        break
    trackCounter = trackCounter + 1
"""
total_ticks = 0
for sub in pattern[trackNum]:
    if isinstance(sub, midi.events.NoteOnEvent) or isinstance(sub, midi.events.NoteOffEvent):
        total_ticks = sub
"""

trumpet = pattern[trackNum]
pattern.remove(trumpet)
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
for bpm in bpms:
    tempo_event = midi.events.SetTempoEvent()
    tempo_event.set_bpm(bpm.bp)
    track.append(tempo_event)
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
        off.velocity = note.velocity
        off.pitch = note.pitch
        track.append(off)
eot = midi.EndOfTrackEvent()
eot.tick = 1
track.append(eot)

midi.write_midifile("demo.mid", new_trumpet)

pygame.mixer.music.load("demo.mid")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)

""""
midi.write_midifile("backingsong.mid", pattern)

pygame.mixer.music.load("backingsong.mid")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
   pygame.time.wait(1000)
"""
