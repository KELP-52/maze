from pygame import *
font.init()

size = (700, 400)
window = display.set_mode(size)
display.set_caption("Лабиринт")
background = image.load("m1000x1000.jpg")
background = transform.scale(background, size)

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, speed, width, height):
        self.img = image.load(img)
        self.width = width
        self.height = height
        self.img = transform.scale(self.img, (self.width, self.height))
        self.speed = speed
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))
    
class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed 
        if keys_pressed[K_s] and self.rect.y < (size[1] - self.height):
            self.rect.y += self.speed
        if keys_pressed[K_d] and self.rect.x < (size[0] - self.width):
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def end(self, text, color):
        font1 = font.Font(None, 110)
        message = font1.render(text, True, color)
        window.blit(message,(190,155)) 
        
class Enemy(GameSprite):
    def __init__(self, img, x, y, speed, width, height, direction):
        super().__init__(img, x, y, speed, width, height)
        self.direction = direction

    def move_up_down(self):
        if self.rect.y <= 210:
            self.direction = "Up"
        elif self.rect.y >= 330:
            self.direction = "Down"
        if self.direction == "Up":
            self.rect.y += self.speed
        elif self.direction == 'Down':
            self.rect.y -= self.speed

    def move_left_right(self):
        if self.rect.x >= 630:
            self.direction = "Left"
        elif self.rect.x <= 500:
            self.direction = "Right"
        if self.direction == "Left":
            self.rect.x -= self.speed
        elif self.direction == 'Right':
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.img = Surface((width, height))
        self.img.fill(color)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw_wall(self):
        window.blit(self.img, (self.rect.x, self.rect.y))

walls = [
    Wall(100, 0, 10, 315, (0, 255, 0)),
    Wall(200, 100, 10, 315, (0, 255, 0)),
    Wall(100, 0, 700, 10, (0,255, 0)),
    Wall(200, 100, 85, 10, (0, 255, 0)),
    Wall(380, 00, 10, 300, (0, 255, 0)),
    Wall(285, 200, 10, 100, (0, 255, 0)),
    Wall(285, 200, 95, 10, (0, 255, 0)),
    Wall(100, 390, 700, 10, (0, 255, 0)),
    Wall(480, 130, 10, 300, (0, 255, 0)),
    Wall(480, 130, 100, 10, (0, 255, 0)),
    Wall(690, 0, 10, 700, (0, 255, 0)),
    Wall(590, 240, 100, 10, (0, 255, 0))
]
    
player = Player("hero.png", 10, 15, 2, 50, 50)
bad_player_1 = Enemy("cyborg.png", 600, 250, 1, 65, 65, "Right")
bad_player_2 = Enemy("cyborg.png", 305, 200, 1, 65, 65, "Down")
gold = GameSprite("treasure.png", 650, 350, 0, 40, 40)

clock = time.Clock()
game = True
finish = False

while game:
    events = event.get()
    window.blit(background, (0, 0))
    player.draw()
    bad_player_1.draw()
    bad_player_2.draw()
    gold.draw()
    for wall in walls:
        wall.draw_wall()

    if not finish:
        player.move()
        bad_player_1.move_left_right()
        bad_player_2.move_up_down()

    if sprite.collide_rect(player, bad_player_1):
        finish = True
        player.end("you lose", (255, 0, 0))
              
    if sprite.collide_rect(player, bad_player_2):
        finish = True
        player.end("you lose", (255, 0, 0))

    if sprite.collide_rect(player, gold):
        finish = True
        player.end("you won", (255, 0, 255))
    
    for wall in walls:
        if sprite.collide_rect(player,wall):
            finish = True
            player.end("you lose", (255, 0, 0))

    for e in events: 
        if e.type == QUIT:
            game = False
    display.update()
    clock.tick(120)
