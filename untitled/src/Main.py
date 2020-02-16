import sys
import pygame
from os import path

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

size = width, height = 960, 540
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Trumpet Hero")

img_dir = path.join(path.dirname(__file__) + "/images")
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()

circle = pygame.image.load(path.join(img_dir, "circle.png")).convert()
circle_lit = pygame.image.load(path.join(img_dir, "circle_lit.png")).convert()

note1 = pygame.image.load(path.join(img_dir, "note1.png")).convert()
note2 = pygame.image.load(path.join(img_dir, "note2.png")).convert()
note3 = pygame.image.load(path.join(img_dir, "note3.png")).convert()

font_name = pygame.font.match_font('impact')

score = 0

notesArray = []
notesGroup = pygame.sprite.Group()

def start() :

    while 1 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_SPACE]: game()
        screen.blit(background, [0, 0])
        draw_text(screen, str("PRESS SPACE TO START"), 40, width / 2, height / 2)
        pygame.display.flip()

def game():
    global score
    global notesArray
    global notesGroup
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
    tick = 0

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
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
        draw_text(screen, "SCORE: " + str(score), 80, width / 2, 0)
        pygame.display.flip()
        tick += 1
        if tick == 500:
            createNote("red")
            tick = 0

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
        self.image = pygame.transform.scale(image, (60, 60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = 30
        self.rect.centerx = x
        self.speedy = 1
        self.click = 0
    def update(self):
        global score
        #460 = beginning of target
        #530 = end of target
        self.click += 1
        if self.click == 2:
          self.click = 0
          self.rect.y += self.speedy
        if self.rect.bottom > 600:
            score -= 1
            notesArray.remove(self)
            self.kill()

    def checkPressed(self, color):
        global score
        if self.color == color and self.rect.bottom > 430 and self.rect.bottom < 550:
            notesArray.remove(self)
            self.kill()
            score += 1
            return True

        return False

def pause():
    print"paused"
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_ESCAPE]:
                    print"resumed"
                    paused = False

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
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