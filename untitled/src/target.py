import sys
import lib

from Fingerings import GetNoteAndFingering

sys.path.insert(0, "../lib")
import midi
import pygame
import Note

pygame.init()

pattern = midi.read_midifile("music/bohemian.mid")

bpms = []

timeSigCounter = 0

for sub in pattern[0]:
    if isinstance(sub, midi.events.SetTempoEvent):
        bpm = Note.bpm()
        bpm.bp = sub.get_bpm()
        # print(bpm.bp)
        # print(sub.get_mpqn())
        bpm.ticks = sub.tick
        bpms.append(bpm)
    elif isinstance(sub, midi.events.TimeSignatureEvent):
        bpms[timeSigCounter].bp = bpms[timeSigCounter].bp * (sub.data[0] / sub.data[1])
        # print(sub.numerator)
        # print(sub.denominator)
        # print(bpms[timeSigCounter].bp)

# print pattern

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


counter = 0
restCounter = 0
totalTicks = 0

for note in notes:
    if note.duration > 100:
        print('REST', restCounter)
        restCounter = 0

        noteDetails = GetNoteAndFingering(note.pitch)
        print(noteDetails, note.duration)
        counter = counter + 1
    else:
        restCounter = restCounter + note.duration

    totalTicks = totalTicks + note.duration

print('\n')
print('Number of Notes', counter)
print('Number of Total Ticks', totalTicks)

midi.write_midifile("demo.mid", new_trumpet)

pygame.mixer.music.load("demo.mid")
pygame.mixer.music.play()
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
