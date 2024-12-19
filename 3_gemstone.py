# gem image setting
import os
import pygame

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

running = True
while running:
    clock.tick(30) # FPS set to 30

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen) # all of sprites within the group gets drawn into the screen

    pygame.display.update()

pygame.quit()