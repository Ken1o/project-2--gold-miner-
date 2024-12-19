# firing the claw
# firing the claw from the present location
# making it so that when the claw goes off the screen it comes back to original location
# firing speed, returning speed
import os
import pygame

# claw class
class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.original_image = image
        self.rect = image.get_rect(center=position)

        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.position = position

        self.direction = LEFT # claw's moving direction
        self.angle_speed = 2.5 # claw's angle change (swinging speed)
        self.angle = 10 # first angle (right end)

    def update(self, to_x):
        if self.direction == LEFT: # if the claw is moving to the left
            self.angle += self.angle_speed # increasing the angle by angle speed
        elif self.direction == RIGHT: # if moving to the right
            self.angle -= self.angle_speed

        # if the claw leaves the appropriate angle
        if self.angle > 170:
            self.angle = 170
            self.set_direction(RIGHT)
        elif self.angle < 10:
            self.angle = 10
            self.set_direction(LEFT)

        self.offset.x += to_x
        self.rotate() # rotation


    def rotate(self):
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1) # (which image to rotate, rotation angle, image size (scale))
        offset_rotated = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center=self.position+offset_rotated)

    def set_direction(self, direction):
        self.direction = direction

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5) # drawing a straight line from the pivot to the claw position

    def set_init_state(self):
        self.offset.x = default_offset_x_claw
        self.angle = 10
        self.direction = LEFT

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
to_x = 0 # saving the x pivot coord for how far the image will move

# speed variable
move_speed = 12 # firing speed
return_speed = 20 # when returning with nothing

# direction variable
LEFT = -1 # left direction
RIGHT = 1 # right direction
STOP = 0 

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

        if event.type == pygame.MOUSEBUTTONDOWN: # when clicked with mouse
            claw.set_direction(STOP)
            to_x = move_speed # firing by move_speed speed

    if claw.rect.left < 0 or claw.rect.right > screen_width or claw.rect.bottom > screen_height:
        to_x = -return_speed

    if claw.offset.x < default_offset_x_claw: # when returning to original pivot
        to_x = 0
        claw.set_init_state() # returning to the original state

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen) # all of sprites within the group gets drawn into the screen
    claw.update(to_x)
    claw.draw(screen)

    pygame.display.update()

pygame.quit()