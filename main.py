__author__ = 'Pradyumn Vikram'

# imports
import pygame
import os
import random

# some variables
width = 300
height = 490

pygame.init()

font = pygame.font.SysFont('comicsans', 25)
over_font = pygame.font.SysFont('sans serif', 50)
win = pygame.display.set_mode((width, height))
root = os.path.dirname(__file__)

life = pygame.image.load(os.path.join(root, 'data\\life_heart.png'))
bg = pygame.image.load(os.path.join(root, 'data\\background.jpg'))


# the player class
class Player:

    def __init__(self, x, y, Pwidth, Pheight, vel, color):
        self.x = x
        self.y = y
        self.width = Pwidth
        self.vel = vel
        self.height = Pheight
        self.color = color

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, key):
        if key == 'ra_mr':
            self.x += self.vel
        elif key == 'la_ml':
            self.x -= self.vel

    def draw(self, window):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, self.color, self.rect)


# the object class
class CatchObject:

    def __init__(self, color):
        self.radius = random.randint(5, 10)
        self.x = random.randint(self.radius * 2, width - self.radius * 2)
        self.y = 0 - self.radius * 2
        self.color = color
        self.circle_rect = None
        self.vel = random.randint(3, 7)

    def draw(self, window):
        if self.radius == 3:
            self.color = (255, 215, 0)
            self.vel = 7
            self.circle_rect = pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
        else:
            self.circle_rect = pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.y += self.vel


# just another collision test
def collide(obj1, obj2):
    if obj1.rect.colliderect(obj2.circle_rect):
        return True
    return False


# display update and stuff
def redraw_window(window, player, objects, score, lives):
    window.fill((0, 0, 0))
    window.blit(bg, (0, 0))
    Xval = 10
    for _ in range(lives):
        window.blit(life, (Xval, 0))
        Xval += 10

    label = font.render('Score: ' + str(score), 1, (14, 42, 85))
    window.blit(label, (width - label.get_width() - 10, 0))
    player.draw(window)
    if lives == 0:
        labelx = over_font.render('GAME OVER!', 1, (178, 25, 25))
        win.blit(labelx, (width // 2 - 110, height // 2))
    for Cobject in objects:
        Cobject.draw(window)
        Cobject.move()
    pygame.display.update()


# the main loop!
def main():
    score = 0
    lives = 6
    player = Player(150, height - 30, 50, 10, 5, (3, 126, 140))
    clock = pygame.time.Clock()
    pause = False
    objects = [CatchObject((232, 75, 95))]
    scores = {5: 10,
              6: 9,
              7: 8,
              8: 7,
              9: 6,
              10: 5}
    while True:
        clock.tick(60)
        redraw_window(win, player, objects, score, lives)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(-1)
        if not pause:
            for ind, Cobject in enumerate(objects):
                if Cobject.y > height and not pause:
                    lives -= 1
                    objects.pop(ind)
                    if lives == 0:
                        pause = True
                if collide(player, Cobject):
                    if Cobject.color == (255, 215, 0):
                        score += 150
                    else:
                        score += scores[Cobject.radius] * Cobject.vel
                    objects.pop(ind)

            if len(objects) == 0:
                objects.append(CatchObject((232, 75, 95)))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT] and player.x + player.width + 4 < width:
                player.move('ra_mr')
            if keys[pygame.K_LEFT] and player.x + 4 > 0:
                player.move('la_ml')


#main menu and combining everything
def main_menu():
    run = True
    title_font = pygame.font.SysFont('arial', 28)

    while run:
        win.fill((252, 209, 42))
        intro = title_font.render('Press mouse button to start!', 1, (50, 50, 50))
        win.blit(intro, (int(width / 2 - intro.get_width() / 2), 210))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


#running the loop!
main_menu()
