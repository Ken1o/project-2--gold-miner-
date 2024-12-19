import os
import pygame

# claw class
class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)

        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.position = position

    def update(self):
        rect_center = self.position + self.offset
        self.rect = self.image.get_rect(center=rect_center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, BLACK, self.position, 3)
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5) # drawing a straight line from the pivot to the claw position

# gemstone class
class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)

def setup_gemstone():
    # small_gold
    small_gold = Gemstone(gemstone_images[0], (200, 380)) # 0th image is places at (200, 380)
    gemstone_group.add(small_gold) # adding to the group
    # big gold
    gemstone_group.add(Gemstone(gemstone_images[1], (300, 500)))
    # stone
    gemstone_group.add(Gemstone(gemstone_images[2], (300, 380)))
    # diamond
    gemstone_group.add(Gemstone(gemstone_images[3], (900, 420)))


pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")
clock = pygame.time.Clock()

# game related variable
default_offset_x_claw = 40

# color variable
BLACK = (0, 0, 0) # RGB

# getting the background image
current_path = os.path.dirname(__file__) # location of present file
background = pygame.image.load(os.path.join(current_path, "background.png"))

# 4 different gems(small gold, big gold, stone, diamond)
gemstone_images = [
    pygame.image.load(os.path.join(current_path, "small_gold.png")), # small gold
    pygame.image.load(os.path.join(current_path, "big_gold.png")), # big gold
    pygame.image.load(os.path.join(current_path, "stone.png")), # stone
    pygame.image.load(os.path.join(current_path, "diamond.png"))] # diamond

# gem group
gemstone_group = pygame.sprite.Group()
setup_gemstone() # defining number of gems the game wants

# claw
claw_image = pygame.image.load(os.path.join(current_path, "claw.png"))
claw = Claw(claw_image, (screen_width // 2, 110)) # width will be half screen width, height will be 110px from the top

running = True
while running:
    clock.tick(30) # FPS set to 30

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen) # all of sprites within the group gets drawn into the screen
    claw.update()
    claw.draw(screen)

    pygame.display.update()

pygame.quit()