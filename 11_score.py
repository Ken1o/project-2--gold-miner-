# game score
# aim score(1500)
# present score (?)
import os
import math
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
    def __init__(self, image, position, price, speed):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.price = price
        self.speed = speed

    def set_position(self, position, angle):
        r = self.rect.size[0] // 2 # radius
        rad_angle = math.radians(angle) # angle
        to_x = r * math.cos(rad_angle) # triangle's width
        to_y = r * math.sin(rad_angle) # triangle's height

        self.rect.center = (position[0] + to_x, position[1] + to_y) 

def setup_gemstone():
    small_gold_price, small_gold_speed = 100, 5
    big_gold_price, big_gold_speed = 300, 2
    stone_price, stone_speed = 10, 2
    diamond_price, diamond_speed = 600, 7

    # small_gold
    small_gold = Gemstone(gemstone_images[0], (200, 380), small_gold_price, small_gold_speed) # 0th image is places at (200, 380)
    gemstone_group.add(small_gold) # adding to the group
    # big gold
    gemstone_group.add(Gemstone(gemstone_images[1], (300, 500), big_gold_price, big_gold_speed))
    # stone
    gemstone_group.add(Gemstone(gemstone_images[2], (300, 380), stone_price, stone_speed))
    # diamond
    gemstone_group.add(Gemstone(gemstone_images[3], (900, 420), diamond_price, diamond_speed))

def update_score(score):
    global current_score
    current_score += score

def display_score():
    txt_current_score = game_font.render(f"Current Score: {current_score:,}", True, BLACK)
    screen.blit(txt_current_score, (50, 20))

    txt_goal_score = game_font.render(f"Aim Score: {goal_score:,}", True, BLACK)
    screen.blit(txt_goal_score, (50, 80))


pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("arialrounded", 30)

# score related variable
goal_score = 1500 # aim score
current_score = 0 # current score

# game related variable
default_offset_x_claw = 40
to_x = 0 # saving the x pivot coord for how far the image will move
caught_gemstone = None # saving the gemstone which is caught by the claw

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
    pygame.image.load(os.path.join(current_path, "small_gold.png")).convert_alpha(), # small gold
    pygame.image.load(os.path.join(current_path, "big_gold.png")).convert_alpha(), # big gold
    pygame.image.load(os.path.join(current_path, "stone.png")).convert_alpha(), # stone
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

        if caught_gemstone: # if caught
            update_score(caught_gemstone.price) # score update
            gemstone_group.remove(caught_gemstone) # removing the caught gemstone
            caught_gemstone = None

    if not caught_gemstone: # when no gemstone was caught
        for gemstone in gemstone_group:
            # if claw.rect.colliderect(gemstone.rect): # only for rectangle not the whole image
            if pygame.sprite.collide_mask(claw, gemstone): # colliding when it actually hits the image
                caught_gemstone = gemstone # information of caught gemstone
                to_x = -gemstone.speed # speed of the caught gemstone, it is - because going back to the pivot
                break

    if caught_gemstone:
        caught_gemstone.set_position(claw.rect.center, claw.angle)

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen) # all of sprites within the group gets drawn into the screen
    claw.update(to_x)
    claw.draw(screen)

    # presenting the score
    display_score()


    pygame.display.update()

pygame.quit()