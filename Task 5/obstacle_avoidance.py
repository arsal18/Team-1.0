import pygame
import math

# Constants for the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Constants for car properties
CAR_SIZE = 30
CAR_SPEED = 0.5

# Constants for obstacle properties
OBSTACLE_RADIUS = 20
OBSTACLE_COLOR = (55, 55, 55)
OBSTACLE_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Constants for the avoidance maneuver
SAFE_DISTANCE = 100
AVOIDANCE_ANGLE = 90
AVOIDANCE_DISTANCE = OBSTACLE_RADIUS + SAFE_DISTANCE

# Colors for cars in the platoon
CAR_COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0)]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Initialize cars' positions and headings
car_x = SCREEN_WIDTH // 4
car_y = SCREEN_HEIGHT // 2
car_headings = [0, 0, 0]

# Game loop
running = True
start_time = pygame.time.get_ticks()  # Get the start time
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate the time elapsed since the start of the simulation
    elapsed_time = pygame.time.get_ticks() - start_time

    # Clear the screen
    screen.fill((255, 255, 255))

    # Update and draw each car in the platoon
    for i in range(len(CAR_COLORS)):
        # Calculate the distance and angle between the car and the obstacle
        distance = math.sqrt((car_x - OBSTACLE_POSITION[0]) ** 2 + (car_y - OBSTACLE_POSITION[1]) ** 2)
        angle = math.degrees(math.atan2(OBSTACLE_POSITION[1] - car_y, OBSTACLE_POSITION[0] - car_x))

        # Check if the car needs to avoid the obstacle
        if distance <= AVOIDANCE_DISTANCE:
            avoidance_angle = angle + AVOIDANCE_ANGLE
            avoidance_x = OBSTACLE_POSITION[0] + AVOIDANCE_DISTANCE * math.cos(math.radians(avoidance_angle))
            avoidance_y = OBSTACLE_POSITION[1] + AVOIDANCE_DISTANCE * math.sin(math.radians(avoidance_angle))
            target_angle = math.degrees(math.atan2(avoidance_y - car_y, avoidance_x - car_x))
        else:
            target_angle = angle

        # Adjust the car's heading towards the target angle
        angle_diff = target_angle - car_headings[i]
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360
        car_headings[i] += angle_diff * 0.05

        # Move the car based on its heading
        car_x += CAR_SPEED * math.cos(math.radians(car_headings[i]))
        car_y += CAR_SPEED * math.sin(math.radians(car_headings[i]))

        # Draw the car
        car_rect = pygame.Rect(car_x - CAR_SIZE // 2, car_y - CAR_SIZE // 2, CAR_SIZE, CAR_SIZE)
        pygame.draw.rect(screen, CAR_COLORS[i], car_rect)

    # Draw the obstacle
    obstacle_rect = pygame.Rect(OBSTACLE_POSITION[0] - OBSTACLE_RADIUS, OBSTACLE_POSITION[1] - OBSTACLE_RADIUS,
                                OBSTACLE_RADIUS * 2, OBSTACLE_RADIUS * 2)
    pygame.draw.circle(screen, OBSTACLE_COLOR, OBSTACLE_POSITION, OBSTACLE_RADIUS)

    # Update the screen
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

    # Check if the elapsed time exceeds 20 seconds (20000 milliseconds)
    if elapsed_time > 3350:
        running = False

# Quit the game
pygame.q
