import sys
sys.path.insert(0, "../lib")
import midi
import pygame

pygame.init()

pattern = midi.read_midifile("369646.mid")
print(pattern)

pygame.mixer.music.load("369646.mid")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)
print("Hello")