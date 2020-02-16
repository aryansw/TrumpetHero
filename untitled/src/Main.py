import pygame
import sys
import midi
from lib import Leap
import Trumpet
from os import path
import random
import target

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
AQUA = (0, 255, 255)

class SongObj:
    def __init__(self, path, type, threshold, name):
        self.path = path
        self.type = type
        self.threshold = threshold
        self.name = name

DIFFICULTY = "EASY"

size = width, height = 960, 540
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Trumpet Hero")

img_dir = path.join(path.dirname(__file__) + "/images")
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
mainMenuBackground = pygame.image.load(path.join(img_dir, "mainMenuBackground.jpg")).convert()
songSelectBackground = pygame.image.load(path.join(img_dir, "songBackground.jpg")).convert()
logo = pygame.image.load(path.join(img_dir, "logo.png")).convert()

circle = pygame.image.load(path.join(img_dir, "circle.png")).convert()
circle_lit = pygame.image.load(path.join(img_dir, "circle_lit.png")).convert()
circle_played = pygame.image.load(path.join(img_dir, "circle_played.png")).convert()
circle_missed = pygame.image.load(path.join(img_dir, "circle_missed.png")).convert()

note1 = pygame.image.load(path.join(img_dir, "red.png")).convert()
note2 = pygame.image.load(path.join(img_dir, "green.png")).convert()
note3 = pygame.image.load(path.join(img_dir, "blue.png")).convert()

font_name = pygame.font.match_font('impact')

score = 0
score_multiplier = 0
streak = 0
score_threshold = False

notesArray = []
notesGroup = pygame.sprite.Group()

listener = Trumpet.SampleListener()
controller = Leap.Controller()
songArray = []
songArray.append(SongObj("music/bohemian", "Piano", 90, "Bohemian Rhapsody"))
songArray.append(SongObj("music/canon", "Piano", 90, "Canon in D"))
songArray.append(SongObj("music/highway", "Distorted Guitar", 90, "Highway to Hell"))
songArray.append(SongObj("music/mario", "Violin", 90, "Mario"))
songArray.append(SongObj("music/miitheme", "SmartMusic SoftSynth", 90, "Mii Theme"))
songArray.append(SongObj("music/pokemon", "Violin", 90, "Pokemon"))
songArray.append(SongObj("music/pirates", "Piano", 90, "Pirates of the Caribbean"))
songArray.append(SongObj("music/NeverGonnaGiveYouUp", "NEVERGON", 90, "Never Gonna Give You Up"))
songArray.append(SongObj("music/AllStar", "Staff", 50, "All Star"))
songArray.append(SongObj("music/starwars", "BRASS 1", 50, "Star Wars"))
songArray.append(SongObj("music/BillieJean.mid", "Clav/Brass", 50, "Billie Jean"))
currentsong = songArray[1]


def start() :
    global DIFFICULTY

    logoSprite = pygame.sprite.Group()
    logoSprite.add(dummyObj(logo, width / 2, height / 2, 525, 375))
    selection = 0
    upDebounce = False
    downDebounce = False

    while 1 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_ESCAPE]: sys.exit()
                if pressed[pygame.K_SPACE] and selection == 0: song_select()
                if pressed[pygame.K_w]:
                    selection += 1
                    if selection >= 2:
                        selection = 0
                if pressed[pygame.K_s]:
                    selection -= 1
                    if selection < 0:
                        selection = 1
                if pressed[pygame.K_d] and selection == 1:
                    if DIFFICULTY == "EASY":
                        DIFFICULTY = "MEDIUM"
                    elif DIFFICULTY == "MEDIUM":
                        DIFFICULTY = "HARD"
                    else:
                        DIFFICULTY = "EASY"
                if pressed[pygame.K_a] and selection == 1:
                    if DIFFICULTY == "EASY":
                        DIFFICULTY = "HARD"
                    elif DIFFICULTY == "MEDIUM":
                        DIFFICULTY = "EASY"
                    else:
                        DIFFICULTY = "MEDIUM"

        screen.blit(mainMenuBackground, [0, 0])
        logoSprite.draw(screen)
        if selection == 0:
            draw_text(screen, str("SONG SELECT"), 30, width / 2, 8 * height / 10, "fancy", YELLOW)
        else:
            draw_text(screen, str("SONG SELECT"), 30, width / 2, 8 * height / 10, "fancy", WHITE)
        if selection == 1:
            draw_text(screen, str("DIFFICULTY: " + DIFFICULTY), 30, width / 2, 9 * height / 10, "fancy", YELLOW)
        else:
            draw_text(screen, str("DIFFICULTY: " + DIFFICULTY), 30, width / 2, 9 * height / 10, "fancy", WHITE)

        pygame.display.flip()

def song_select():
    global currentsong

    selection = 0
    select = True

    while select:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_SPACE]:
                    currentsong = songArray[selection]
                    game()
                if pressed[pygame.K_ESCAPE]: select = False
                if pressed[pygame.K_s]:
                    selection += 1
                    if selection >= len(songArray):
                        selection = 0
                if pressed[pygame.K_w]:
                    selection -= 1
                    if selection < 0:
                        selection = len(songArray) - 1

        screen.blit(songSelectBackground, [0, 0])
        page = selection // 5
        pageLength = 5
        if len(songArray) - page*5 < 5:
            pageLength = len(songArray) - page*5
        for i in range(page*5, page*5 + pageLength):
            n = i - (5*page)
            if selection % 5 == n:
                draw_text(screen, songArray[i].name, 30, width / 2, (n+2) * height / 11, "fancy", YELLOW)
            else:
                draw_text(screen, songArray[i].name, 30, width / 2, (n+2) * height / 11, "fancy", WHITE)

        pygame.display.flip()

def game():
    global score
    global score_multiplier
    global score_threshold
    global streak
    global notesArray
    global notesGroup
    global listener
    global controller
    global currentsong
    notesGroup.empty()
    notesArray = []

    circles = pygame.sprite.Group()
    circleOne = CircleObj(1)
    circleTwo = CircleObj(2)
    circleThree = CircleObj(3)
    circles.add(circleOne)
    circles.add(circleTwo)
    circles.add(circleThree)

    spacePressed = False
    lIndexDebounceFlag = False
    if DIFFICULTY == "EASY":
        tick = 850
    if DIFFICULTY == "MEDIUM":
        tick = 285
    if DIFFICULTY == "HARD":
        tick = 170

    controller.add_listener(listener)
    lIndexPressed = False
    rIndexPressed = False
    middlePressed = False
    ringPressed = False
    hasStarted = False
    score_multiplier = 1
    streak = 0
    score = 0

    threshold = 90
    if DIFFICULTY == "MEDIUM":
        threshold = 75
    if DIFFICULTY == "HARD":
        threshold = 60

    song = target.GetNoteSequence(currentsong.path + ".mid", currentsong.type, threshold)
    songLength = len(song)
    blockNum = 0

    #0 = pygame.mixer.Channel(0)
    #channel1 = pygame.mixer.Channel(1)
    pygame.mixer.music.load(currentsong.path + ".mid")
    pygame.mixer.music.play()
    """
    backgroundMusic = pygame.mixer.Sound(currentsong.path + "back.wav")
    trumpetMusic = pygame.mixer.Sound(currentsong.path + ".wav")
    channel1.play(backgroundMusic)
    channel0.play(trumpetMusic)
    channel1.set_volume(0.7)
    channel1.pause()
    channel1.unpause()
    """
    while tick > song[blockNum].duration:
        tick -= song[blockNum].duration
        blockNum += 1

    game = True
    while game:
        if streak >= 40:
            score_multiplier = 8
        elif streak >= 30:
            score_multiplier = 4
        elif streak >= 20:
            score_multiplier = 3
        elif streak >= 10:
            score_multiplier = 2
        else:
            score_multiplier = 1

        if streak == 0 and hasStarted:
            pygame.mixer.music.set_volume(0.5)
            #channel0.set_volume(0)
            #channel1.set_volume(0.7)
        elif streak >= 1:
            hasStarted = True
            #channel0.set_volume(1)
            pygame.mixer.music.set_volume(1)

        [lIndexPressed, rIndexPressed, middlePressed, ringPressed, sawLeft] = listener.check_frame(controller)
        if rIndexPressed and not circleThree.pressed:
            circleThree.press()
        elif not rIndexPressed and circleThree.pressed:
            circleThree.release()

        if middlePressed and not circleTwo.pressed:
            circleTwo.press()
        elif not middlePressed and circleTwo.pressed:
            circleTwo.release()

        if ringPressed and not circleOne.pressed:
            circleOne.press()
        elif not ringPressed and circleOne.pressed:
            circleOne.release()

        if lIndexPressed and not lIndexDebounceFlag:
            lIndexDebounceFlag = True
            if circleOne.pressed:

                found = False
                for note in notesArray:
                    found = note.checkPressed("red")
                    if found:
                        break
                if not found:
                    score -= 1
                    streak = 0
                    score_multiplier = 1
                    score_threshold = True
                    circleOne.miss()
                else:
                    circleOne.play()

            if circleTwo.pressed:
                found = False
                for note in notesArray:
                    found = note.checkPressed("green")
                    if found:
                        break
                if not found:
                    score -= 1
                    streak = 0
                    score_multiplier = 1
                    score_threshold = True
                    circleTwo.miss()
                else:
                    circleTwo.play()

            if circleThree.pressed:
                found = False
                for note in notesArray:
                    found = note.checkPressed("blue")
                    if found:
                        break
                if not found:
                    score -= 1
                    streak = 0
                    score_multiplier = 1
                    score_threshold = True
                    circleThree.miss()
                else:
                    circleThree.play()

        if not lIndexPressed and lIndexDebounceFlag:
            if circleOne.pressed:
                circleOne.press()
            if circleTwo.pressed:
                circleTwo.press()
            if circleThree.pressed:
                circleThree.press()
            lIndexDebounceFlag = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                controller.remove_listener(listener)
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_ESCAPE]:
                    #pygame.mixer.music.pause()
                    game = False
                """
                #if pressed[pygame.K_SPACE]: score = score + 1
                if pressed[pygame.K_q]: circleOne.press()
                if pressed[pygame.K_w]: circleTwo.press()
                if pressed[pygame.K_e]: circleThree.press()
                if not spacePressed and pressed[pygame.K_SPACE]:
                    if circleOne.pressed:
                        found = False
                        for note in notesArray:
                            found = note.checkPressed("red")
                            if found:
                                break
                        if not found:
                            score -= 1

                    if circleTwo.pressed:
                        found = False
                        for note in notesArray:
                            found = note.checkPressed("green")
                            if found:
                                break
                        if not found:
                            score -= 1

                    if circleThree.pressed:
                        found = False
                        for note in notesArray:
                            found = note.checkPressed("blue")
                            if found:
                                break
                        if not found:
                            score -= 1
                    print len(notesArray)
                    spacePressed = True
            if event.type == pygame.KEYUP:
                pressed = pygame.key.get_pressed()
                if circleOne.pressed and not pressed[pygame.K_q]:
                    circleOne.release()
                if circleTwo.pressed and not pressed[pygame.K_w]:
                    circleTwo.release()
                if circleThree.pressed and not pressed[pygame.K_e]:
                    circleThree.release()
                if spacePressed and not pressed[pygame.K_SPACE]:
                    spacePressed = False
            """
        screen.fill(BLACK)
        screen.blit(background, [0, 0])
        notesGroup.update()
        notesGroup.draw(screen)
        circles.draw(screen)
        if score < 0:
            score = 0

        if not sawLeft:
            draw_text(screen, "NO LEFT", 50, width / 8, 0, "normal", RED)
            draw_text(screen, "HAND " + str(tick), 50, width / 8, 75, "normal", RED)
        draw_text(screen, "SCORE: " + str(score), 80, width / 2, 0, "normal", BLACK)
        draw_text(screen, "STREAK: " + str(streak), 50, 7 * width / 8, 0, "normal", AQUA)
        draw_text(screen, "MULTIPLIER: " + str(score_multiplier) + "x", 40, 7* width / 8, 75, "normal", AQUA)
        pygame.display.flip()
        tick += 1
        if tick == song[blockNum].duration:
            if not song[blockNum].isRest:
                if song[blockNum].finger[0] == 1:
                    createNote("red")
                if song[blockNum].finger[1] == 1:
                    createNote("green")
                if song[blockNum].finger[2] == 1:
                    createNote("blue")
            blockNum += 1
            tick = 0
            if blockNum > len(song):
                game = False

    #channel1.stop()
    #0.stop()
    #backgroundMusic.stop()
    pygame.mixer.music.stop()


class dummyObj(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scaleX, scaleY):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image = pygame.transform.scale(image, (scaleX, scaleY))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x


class CircleObj(pygame.sprite.Sprite):
    def __init__(self, position):
        self.position = position
        self.pressed = False
        pygame.sprite.Sprite.__init__(self)
        image = circle
        self.image = image
        self.image = pygame.transform.scale(image, (100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = 460
        if (position == 1):
            self.rect.centerx = width / 2 - 120
        elif (position == 3):
            self.rect.centerx = width / 2 + 120
        else:
            self.rect.centerx = width / 2

    def press(self):
        position = self.position
        self.pressed = True
        image = circle_lit
        self.image = image
        self.image = pygame.transform.scale(image, (100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = 460
        if (position == 1):
            self.rect.centerx = width / 2 - 120
        elif (position == 3):
            self.rect.centerx = width / 2 + 120
        else:
            self.rect.centerx = width / 2

    def release(self):
        position = self.position
        self.pressed = False
        image = circle
        self.image = image
        self.image = pygame.transform.scale(image, (100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = 460
        if (position == 1):
            self.rect.centerx = width / 2 - 120
        elif (position == 3):
            self.rect.centerx = width / 2 + 120
        else:
            self.rect.centerx = width / 2

    def play(self):
        position = self.position
        self.pressed = True
        image = circle_played
        self.image = image
        self.image = pygame.transform.scale(image, (100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = 460
        if (position == 1):
            self.rect.centerx = width / 2 - 120
        elif (position == 3):
            self.rect.centerx = width / 2 + 120
        else:
            self.rect.centerx = width / 2

    def miss(self):
        position = self.position
        self.pressed = True
        image = circle_missed
        self.image = image
        self.image = pygame.transform.scale(image, (100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = 460
        if (position == 1):
            self.rect.centerx = width / 2 - 120
        elif (position == 3):
            self.rect.centerx = width / 2 + 120
        else:
            self.rect.centerx = width / 2

class NoteObj(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.scaleFactor = 60
        if color == "red":
            x = (width / 2) - 120
            image = note1
        if color == "green":
            x = width / 2
            image = note2
        if color == "blue":
            x = width / 2 + 120
            image = note3
        self.image = image
        self.image.set_colorkey(BLACK)
        #self.image = pygame.transform.scale(image, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.centery = 30
        self.rect.centerx = x
        if DIFFICULTY == "EASY":
            self.speedy = 1
        if DIFFICULTY == "MEDIUM":
            self.speedy = 3
        if DIFFICULTY == "HARD":
            self.speedy = 5
        self.click = 0

    def update(self):
        global score
        global streak
        global score_multiplier
        global  score_threshold
        #460 = beginning of target
        #530 = end of target
        self.click += 1
        if self.click == 2:
          self.click = 0
          self.rect.y += self.speedy
        if self.rect.bottom > 600:
            score -= 1
            streak = 0
            score_multiplier = 1
            score_threshold = True
            notesArray.remove(self)
            self.kill()

    def checkPressed(self, color):
        global score
        global streak
        global score_threshold
        if self.color == color and self.rect.bottom > 430 and self.rect.bottom < 550:
            notesArray.remove(self)
            self.kill()
            score += 1 * score_multiplier
            streak += 1
            score_threshold = False
            return True

        return False

"""
def pause():
    global listener
    global controller

    print"paused"
    paused = True
    while paused:
        draw_text(screen, "SCORE: " + str(score), 80, width / 2, 0, "normal", BLACK)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                controller.remove_listener(listener)
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_p]:
                    print"resumed"
                    paused = False
                    return True
                if pressed[pygame.K_ESCAPE]:
                    paused = False
                    return False
"""

def draw_text(surf, text, size, x, y, font, color):
    if font == "normal":
        font = pygame.font.Font(font_name, size)
    if font == "fancy":
        font = pygame.font.Font(pygame.font.match_font('ebrima'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def createNote(color):
    global notesArray
    global notesGroup
    newNote = NoteObj(color)
    notesGroup.add(newNote)
    notesArray.append(newNote)


if __name__ == "__main__":
    start()