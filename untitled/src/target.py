import midi

pattern = midi.read_midifile("../369646.mid")



tracks = []

trackCounter = 0
for track in pattern:
    tracks.append(track)

    if trackCounter == 5:
        print(tracks[trackCounter])

    trackCounter = trackCounter + 1


if isinstance(tracks[0][0], midi.events.TrackNameEvent):
    print("It is the same")