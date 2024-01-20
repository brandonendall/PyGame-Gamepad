import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height),pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("Virtual Gamepad Controller")


# Load PNG images for the D-pad and buttons
dpad_image = pygame.image.load("buttons/Dpad2.png").convert_alpha()
dpad_image = pygame.transform.rotozoom(dpad_image,0,0.35)

a_button_image = pygame.image.load("buttons/A_button2.png").convert_alpha()
a_button_image = pygame.transform.rotozoom(a_button_image,0,0.70)


b_button_image = pygame.image.load("buttons/B_button2.png").convert_alpha()
b_button_image = pygame.transform.rotozoom(b_button_image,0,0.70)

c_button_image = pygame.image.load("buttons/C_button2.png").convert_alpha()
c_button_image = pygame.transform.rotozoom(c_button_image,0,0.70)


# Define the virtual D-pad
dpad_size =100
dpad_x = 50
dpad_y = 250
dpad_rect = pygame.Rect(dpad_x, dpad_y, dpad_size, dpad_size)

# Define the A/B buttons
button_size = 50
a_button_rect = pygame.Rect(620, 315, button_size, button_size)
b_button_rect = pygame.Rect(645, 245, button_size, button_size)
c_button_rect = pygame.Rect(715, 220, button_size, button_size)

# Define the Game Boy display area
display_width = 800
display_height = 400
display_x = (screen_width - display_width) // 2
display_y = 0
display_rect = pygame.Rect(display_x, display_y, display_width, display_height)

# Load an image for the object to be moved
object_image = pygame.Surface((30, 30))
object_image.fill("black")
object_rect = object_image.get_rect()
object_rect.center = (screen_width // 2, screen_height // 2)

# Set initial object movement
object_speed = 5
object_movement = [0, 0]

# Background
sky_surf = pygame.image.load("graphics/Land.png").convert()
sky_surf = pygame.transform.scale(sky_surf, (800, 400))

fingers = {} # for storing our multiple touches on the screen

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

         # Collecting our multiple touches and making key value pair of it dont use MOUSEBUTTONDOWN as we only have 1 mouse
        if event.type == pygame.FINGERDOWN:
            x = event.x * screen.get_width() #x pos * width of screen
            y = event.y * screen.get_height() #y pos * height of screen
            fingers[event.finger_id] = x, y #storing in fingers dict
        # Removing the touch positions after we remove the finger/fingers
        if event.type == pygame.FINGERUP:
            fingers.pop(event.finger_id, None)
            object_movement = [0, 0]  # Stop object movement when D-pad is released


     #iterating over the fingers dictionary and changing the player location to move it
    for finger, pos in fingers.items(): #finger is finger id i guess and pos is the position of our finger
        if dpad_rect.collidepoint(pos):             
                # Adjust the object's movement based on D-pad direction
            if pos[0] < dpad_x + dpad_size / 3:
                object_movement[0] = -object_speed  # Move left
            elif pos[0] > dpad_x + 2 * dpad_size / 3:
                object_movement[0] = object_speed  # Move right
            if pos[1] < dpad_y + dpad_size / 3:
                object_movement[1] = -object_speed  # Move up
            elif pos[1] > dpad_y + 2 * dpad_size / 3:
                object_movement[1] = object_speed  # Move down
        elif a_button_rect.collidepoint(pos):
            print("A button pressed")
            object_image.fill("red")
        elif b_button_rect.collidepoint(pos):
            print("B button pressed")
            object_image.fill("blue")
        elif c_button_rect.collidepoint(pos):
            print("C button pressed")
            object_image.fill("green")


    # Move the object based on the calculated movement, but constrain it within the grey area
    object_rect = object_rect.move(object_movement)
    object_rect.clamp_ip(display_rect)

    # Clear the screen
    screen.fill("white")

    # Draw the Game Boy display area
    pygame.draw.rect(screen, "gray", display_rect)

    # Draw the D-pad and buttons
    pygame.draw.ellipse(screen, "gray32", dpad_rect)
    pygame.draw.ellipse(screen, "gray32", a_button_rect)
    pygame.draw.ellipse(screen, "gray32", b_button_rect)
    pygame.draw.ellipse(screen, "gray32", c_button_rect)

    # Draw the object, D-pad and buttons using the loaded images
    screen.blit(sky_surf,(0,0))
    screen.blit(object_image, object_rect)
    screen.blit(dpad_image, (30, 230))
    screen.blit(a_button_image, a_button_rect)
    screen.blit(b_button_image, b_button_rect)
    screen.blit(c_button_image, c_button_rect)



    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()