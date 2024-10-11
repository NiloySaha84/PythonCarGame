# Import the necessary modules from pygame and other libraries
import pygame
from pygame.locals import *
import random

# Additional key constants imported from pygame for key event handling
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Set the width and height of the game window
width = 600
height = 600

# Define colors used in the game (RGB values)
Green = (79, 235, 52)  # Background
Gray = (167, 168, 167)  # Road
White = (255, 255, 255)  # Lane markers and text
Yellow = (207, 197, 21)  # Road boundary lines

# Set initial game states and parameters
gameover = False
speed = 2  # Initial speed of the other cars
score = 0  # Player score

# Set up the game clock for managing frames per second (fps)
clock = pygame.time.Clock()
fps = 120  # Frames per second
running = True

# Initial position of the moving lane markers
lane_marker_move_y = 0

# Define the size of the game window and create the display surface
screenSize = (width, height)
screen = pygame.display.set_mode(screenSize)

# Define the Vehicle class that represents the player and other cars
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scale):
        super().__init__()
        self.original_image = image
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.scale = scale
        # Scale the image of the vehicle
        self.image = pygame.transform.scale(self.original_image,
                                            (int(self.original_image.get_rect().width * self.scale),
                                             int(self.original_image.get_rect().height * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Load the images for the player and other vehicles
image = pygame.image.load("/Users/niloysaha/Downloads/car2.png")
other_car_images = [pygame.image.load("/Users/niloysaha/Downloads/otherCar.png"),
                    pygame.image.load("/Users/niloysaha/Downloads/otherCar2.png"),
                    pygame.image.load("/Users/niloysaha/Downloads/otherCar3.png")]

# Load the crash explosion image and scale it to the appropriate size
crash = pygame.transform.scale(pygame.image.load("/Users/niloysaha/Downloads/explosion2.png"), (200, 200))
crash_rect = crash.get_rect()

# Create the player object (car) using the Vehicle class
player = Vehicle(image, 207, 500, 0.15)

# Create a group to hold the other cars (enemies)
other_cars = pygame.sprite.Group()

# Function to spawn other cars (randomly on one of the available lanes)
def spawn_other_car():
    lane_x_positions = [200, 300, 400]  # Lane x-coordinates
    available_lanes = lane_x_positions.copy()

    # Prevent overlapping cars in the same lane
    for car in other_cars:
        if car.rect.x - 10 in available_lanes:
            available_lanes.remove(car.rect.x - 10)

    # Randomly choose a lane and spawn a car if there are available lanes
    if available_lanes:
        x = random.choice(available_lanes)
        y = -100  # Spawn car off-screen at the top
        image = random.choice(other_car_images)  # Randomly choose car image
        other_car = Vehicle(image, x + 10, y, 0.1)

        # Ensure other cars don't spawn too close vertically
        for car in other_cars:
            if abs(other_car.rect.y - car.rect.y) < 200:
                other_car.rect.y -= 200

        # Add the car to the group of other cars
        other_cars.add(other_car)

# Spawn the initial set of enemy cars
for _ in range(2):
    spawn_other_car()

# Main game loop
while running:
    # Cap the frame rate to the fps value
    clock.tick(fps)
    
    # Handle events such as quitting the game or key presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit the loop if the player quits
        if event.type == KEYDOWN:
            if event.key == pygame.K_RIGHT:
                new_x = player.rect.x + 100  # Move the player right by one lane
                if new_x < 350 and gameover == False:
                    player.rect.x = new_x
            elif event.key == pygame.K_LEFT:
                new_x = player.rect.x - 100  # Move the player left by one lane
                if new_x > 50 and gameover == False:
                    player.rect.x = new_x
        # Check for collision between player and other cars
        for vehicle in other_cars:
            if pygame.sprite.collide_rect(player, vehicle):
                gameover = True
                crash_rect.center = player.rect.center  # Center the crash explosion image on the player

    # Fill the background with green (outside the road)
    screen.fill((Green))

    # Draw the road and lane markers
    pygame.draw.rect(screen, Gray, pygame.Rect(150, 0, 300, 600))  # Main road
    pygame.draw.rect(screen, Yellow, pygame.Rect(145, 0, 20, 600))  # Left boundary
    pygame.draw.rect(screen, Yellow, pygame.Rect(450, 0, 20, 600))  # Right boundary

    # Spawn more enemy cars if there are fewer than 2 on screen
    if len(other_cars) < 2:
        spawn_other_car()

    # Move the enemy cars down the screen and remove them if they go off-screen
    for car in other_cars:
        car.rect.y += speed
        if car.rect.top > height:
            car.kill()  # Remove the car from the game
            score += 1  # Increase the score
            # Gradually increase the game speed up to a maximum value
            if speed < 8:
                speed += 0.1
            else:
                speed = 8
            spawn_other_car()  # Spawn a new enemy car

    # Move the lane markers down the screen
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= 160:
        lane_marker_move_y = 0  # Reset lane marker movement

    # Draw the lane markers
    for y in range(80 * -2, 600, 80 * 2):
        pygame.draw.rect(screen, White, pygame.Rect(250, y + lane_marker_move_y, 20, 80))
        pygame.draw.rect(screen, White, pygame.Rect(350, y + lane_marker_move_y, 20, 80))

    # Display the current score on the screen
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, White)
    text_rect = text.get_rect()
    text_rect.center = (50, 450)
    screen.blit(text, text_rect)

    # Draw the player and the enemy cars
    screen.blit(player.image, player.rect.topleft)
    for car in other_cars:
        screen.blit(car.image, car.rect.topleft)

    # If the game is over, display the crash explosion image
    if gameover == True:
        speed = 0  # Stop all movement
        screen.blit(crash, crash_rect)

    # Update the display with all drawn elements
    pygame.display.flip()

# Quit pygame once the game loop has ended
pygame.quit()
