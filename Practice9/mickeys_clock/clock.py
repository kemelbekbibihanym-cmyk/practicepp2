import pygame
import datetime
import os

pygame.init()
# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
CLOCK_CENTER = (600, 350) # Adjusted to center of screen
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mickey's Clock")

# Asset Loading (Check your paths!)
base = r'C:\Users\user\Desktop\PracticePP2\Practice9\mickeys_clock\images'

def load_and_scale(name, size):
    path = os.path.join(base, name)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

# Load images
try:
    bg = load_and_scale('clock.png', (800, 600))
    mickey = load_and_scale('mUmrP.png', (350, 350))
    # Requirement: Right hand = minutes, Left hand = seconds
    hand_min_base = load_and_scale('hand_right_centered.png', (400, 400)) 
    hand_sec_base = load_and_scale('hand_left_centered.png', (400, 400))
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()

clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    now = datetime.datetime.now()
    m = now.minute
    s = now.second

    # --- MATH ---
    # 1. Seconds: 6 degrees per second (360/60)
    # 2. Minutes: 6 degrees per minute
    # Subtracting from 90 or using negative compensates for Pygame's CCW rotation
    # and the fact that 0 deg is '3 o'clock'
    sec_angle = -(s * 6)
    min_angle = -(m * 6 + s * 0.1)

    # --- ROTATION ---
    # Rotate the original base images to avoid quality degradation
    rot_sec = pygame.transform.rotate(hand_sec_base, sec_angle)
    rot_min = pygame.transform.rotate(hand_min_base, min_angle)

    # --- RECT CENTERING ---
    # This is the secret sauce: update the rect center after rotation
    sec_rect = rot_sec.get_rect(center=CLOCK_CENTER)
    min_rect = rot_min.get_rect(center=CLOCK_CENTER)

    # --- DRAWING ---
    screen.fill(WHITE)
    
    # Background
    bg_rect = bg.get_rect(center=CLOCK_CENTER)
    screen.blit(bg, bg_rect)
    
    # Mickey Body
    mic_rect = mickey.get_rect(center=CLOCK_CENTER)
    screen.blit(mickey, mic_rect)

    # Hands
    screen.blit(rot_min, min_rect)
    screen.blit(rot_sec, sec_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()