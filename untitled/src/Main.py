import pygame
import sys
import midi
from lib import Leap
import Trumpet
from os import path
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
DIFFICULTY = "EASY"

size = width, height = 960, 540
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Trumpet Hero")

img_dir = path.join(path.dirname(__file__) + "/images")
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
mainMenuBackground = pygame.image.load(path.join(img_dir, "mainMenuBackground.jpg")).convert()
logo = pygame.image.load(path.join(img_dir, "logo.png")).convert()

circle = pygame.image.load(path.join(img_dir, "circle.png")).convert()
circle_lit = pygame.image.load(path.join(img_dir, "circle_lit.png")).convert()
circle_played = pygame.image.load(path.join(img_dir, "circle_played.png")).convert()
circle_missed = pygame.image.load(path.join(img_dir, "circle_missed.png")).convert()

note1 = pygame.image.load(path.join(img_dir, "redNote.png")).convert()
note2 = pygame.image.load(path.join(img_dir, "greenNote.png")).convert()
note3 = pygame.image.load(path.join(img_dir, "blueNote.png")).convert()

font_name = pygame.font.match_font('impact')

score = 0
score_multiplier = 0
streak = 0
score_threshold = False

notesArray = []
notesGroup = pygame.sprite.Group()

listener = Trumpet.SampleListener()
controller = Leap.Controller()

def start() :
    global DIFFICULTY

    logoSprite = pygame.sprite.Group()
    logoSprite.add(dummyObj(logo, width / 2, height / 3, 450, 350))
    selection = 0
    upDebounce = False
    downDebounce = False

    while 1 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_SPACE]: game()
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
            draw_text(screen, str("SONG SELECT"), 30, width / 2, 6 * height / 10, "fancy", YELLOW)
        else:
            draw_text(screen, str("SONG SELECT"), 30, width / 2, 6 * height / 10, "fancy", WHITE)
        if selection == 1:
            draw_text(screen, str("DIFFICULTY: " + DIFFICULTY), 30, width / 2, 7 * height / 10, "fancy", YELLOW)
        else:
            draw_text(screen, str("DIFFICULTY: " + DIFFICULTY), 30, width / 2, 7 * height / 10, "fancy", WHITE)

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
    circles = pygame.sprite.Group()
    circleOne = CircleObj(1)
    circleTwo = CircleObj(2)
    circleThree = CircleObj(3)
    circles.add(circleOne)
    circles.add(circleTwo)
    circles.add(circleThree)

    createNote("blue")
    createNote("red")
    createNote("green")

    spacePressed = False
    lIndexDebounceFlag = False
    middleDebounceFlag = False
    ringDebounceFlag = False
    tick = 0

    controller.add_listener(listener)
    lIndexPressed = False
    rIndexPressed = False
    middlePressed = False
    ringPressed = False

    while 1:
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
                if pressed[pygame.K_ESCAPE]: pause()
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
        screen.fill(BLACK)
        screen.blit(background, [0, 0])
        notesGroup.update()
        notesGroup.draw(screen)
        circles.draw(screen)
        if not sawLeft:
            draw_text(screen, "NO LEFT", 50, width / 8, 0, "normal", RED)
            draw_text(screen, "HAND", 50, width / 8, 75, "normal", RED)
        draw_text(screen, "SCORE: " + str(score), 80, width / 2, 0, "normal", BLACK)
        draw_text(screen, "STREAK: " + str(streak), 50, 7 * width / 8, 0, "normal", BLACK)
        draw_text(screen, "MULTIPLIER: " + str(score_multiplier) + "x", 40, 7* width / 8, 75, "normal", BLACK)
        pygame.display.flip()
        tick += 1
        if tick == 500:
            diceRoll = random.randint(0, 9)
            if diceRoll < 2:
                createNote("red")
            elif diceRoll < 4:
                createNote("blue")
            elif diceRoll < 6:
                createNote("green")
            elif diceRoll == 6:
                createNote("red")
                createNote("blue")
            elif diceRoll == 7:
                createNote("red")
                createNote("green")
            elif diceRoll == 8:
                createNote("blue")
                createNote("green")
            elif diceRoll == 9:
                createNote("red")
                createNote("blue")
                createNote("green")

            tick = 0

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
        self.image = pygame.transform.scale(image, (75, 75))
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
                if pressed[pygame.K_ESCAPE]:
                    print"resumed"
                    paused = False

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