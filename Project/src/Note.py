import Fingerings


class Tune:
    note = ""
    finger = 0
    duration = 0.0
    pitch = 0
    velocity = 0
    canPlay = False

    def __init__(self, pitch, velocity, duration, canPlay):
        self.note = Fingerings.GetNoteAndFingering(pitch)[0]
        self.finger = Fingerings.GetNoteAndFingering(pitch)[1]
        self.pitch = pitch
        self.velocity = velocity
        self.duration = duration
        self.canPlay = canPlay


class bpm:
    bp = 0.0
    ticks = 0.0


class GameNotes:
    duration = 0.0
    isRest = False
    note = ''
    finger = 0

    def __init__(self, duration, isRest, note, finger):
        self.note = note
        self.finger = finger
        self.isRest = isRest
        self.duration = duration