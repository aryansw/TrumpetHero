import midi

pattern = midi.read_midifile("music/fixyou1.mid")
print pattern
for track in pattern:
    for sub in track:
        if isinstance(sub, midi.events.TextMetaEvent) or isinstance(sub, midi.events.TrackNameEvent):
            instrument = sub.__getattribute__("text")
            print instrument