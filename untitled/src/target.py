import sys
import lib
from mido import MidiFile
from Fingerings import GetNoteAndFingering

sys.path.insert(0, "../lib")
import midi
import pygame
import Note

def GetNoteSequence(filepath, instrumentToMatch, threshold):
    pygame.init()

    pattern = midi.read_midifile(filepath)
    #print pattern
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
            a = 1
            # bpms[timeSigCounter].bp = bpms[timeSigCounter].bp * (sub.data[0] / sub.data[1])
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
                print(instrument)
                if instrument == instrumentToMatch:
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
    midi.write_midifile("backing_song.mid", pattern)
    notes = []

    for event in trumpet:
        # print event
        if isinstance(event, midi.events.NoteOnEvent):
            note = Note.Tune(event.pitch, event.velocity, event.tick, True)
            notes.append(note)
        elif isinstance(event, midi.events.NoteOffEvent):
            note = Note.Tune(event.pitch, 0, event.tick, False)
            notes.append(note)

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
    midi.write_midifile("demo.mid", new_trumpet)
    counter = 0
    restCounter = 0
    totalTicks = 0

    gamenotes = []

    mid = MidiFile('demo.mid')

    for note in notes:
        if note.duration > threshold:
            # print('REST', restCounter)
            gamenote = Note.GameNotes(restCounter, True, '', 0)
            gamenotes.append(gamenote)
            restCounter = 0

            noteDetails = GetNoteAndFingering(note.pitch)
            gamenote = Note.GameNotes(note.duration, False, noteDetails[0], noteDetails[1])
            gamenotes.append(gamenote)
            # print(noteDetails, note.duration)
            counter = counter + 1
        else:
            restCounter = restCounter + note.duration

        totalTicks = totalTicks + note.duration

    mid.type = 1
    seconds = mid.length
    ms_tick = seconds * 1000 / totalTicks

    finalGameNotes = []
    for gamenote in gamenotes:
        if gamenote.duration > 0:
            if gamenote.isRest:
                finalNote = Note.GameNotes(int(gamenote.duration * ms_tick), True, '', 0)
                finalGameNotes.append(finalNote)
                print(finalNote.finger, finalNote.duration)
            else:
                finalNote = Note.GameNotes(int(gamenote.duration * ms_tick), False, gamenote.note, gamenote.finger)
                finalGameNotes.append(finalNote)
                print(finalNote.finger, finalNote.duration)

    # print('\n')
    # print('Number of Notes', counter)
    # print('Number of Total Ticks', totalTicks)
    # print('Length of Song', seconds)

    return finalGameNotes


"""
ns = GetNoteSequence("music/BillieJean.mid", "Clav/Brass", 50)
for note in ns:
    pygame.mixer.music.unpause()
    time = note.duration
    pygame.time.wait(time)
    pygame.mixer.music.pause()
"""


"""
=======
counter = 0
restCounter = 0
totalTicks = 0

gamenotes = []

for note in notes:
    if note.duration > 100:
        print('REST', restCounter)
        gamenote = Note.GameNotes(duration=restCounter, isRest=True)
        gamenotes.append(gamenote)
        restCounter = 0

        noteDetails = GetNoteAndFingering(note.pitch)
        gamenote = Note.GameNotes(note.duration, False, note=noteDetails[0], finger=noteDetails[1])
        gamenotes.append(gamenote)
        print(noteDetails, note.duration)
        counter = counter + 1
    else:
        restCounter = restCounter + note.duration

    totalTicks = totalTicks + note.duration

print('\n')
mid = MidiFile('demo.mid')
mid.type = 1
seconds = mid.length
print('Number of Notes', counter)
print('Number of Total Ticks', totalTicks)
print('Length of Song', seconds)

ms_tick = seconds * 1000 / totalTicks


pygame.mixer.music.load("demo.mid")
pygame.mixer.music.play()
pygame.mixer.music.pause()
counter = 0
for note in gamenotes:
    counter = counter + 1
    pygame.mixer.music.unpause()
    time = int(ms_tick * note.duration)
    pygame.time.wait(time)
    pygame.mixer.music.pause()
"""

""""
midi.write_midifile("backingsong.mid", pattern)

pygame.mixer.music.load("music/369646.mid")
pygame.mixer.music.load("music/bohemian.mid")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
   pygame.time.wait(1000)
"""
