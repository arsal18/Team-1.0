import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pygame

# Example data
data = {
    'truck_id': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
    'truck_color': ['Red', 'Green', 'Blue', 'Green', 'Red', 'Blue', 'Blue', 'Green', 'Red', 'Red', 'Green', 'Blue'],
    'truck_height': [15, 10, 12, 15, 8, 8, 12, 11, 9, 13, 10, 9],
    'truck_width': [10, 8, 9, 10, 8, 10, 12, 11, 11, 10, 9, 10],
    'number_of_sensors': [7, 6, 5, 12, 7, 10, 16, 7, 15, 10, 6, 8],
    'speed': [80, 75, 78, 90, 85, 82, 89, 72, 88, 92, 86, 80]
}

df = pd.DataFrame(data)

# Separate features and labels
features = df[['truck_height', 'truck_width', 'number_of_sensors', 'speed']]
labels = df['truck_color']

# Create the decision tree classifier
clf = DecisionTreeClassifier()

# Train the model
clf.fit(features, labels)

# Example new data for prediction
new_data = {
    'truck_color': ['Red', 'Green', 'Blue'],
    'truck_height': [16, 19, 10],
    'truck_width': [24, 18, 10],
    'number_of_sensors': [18, 20, 11],
    'speed': [60, 195, 180]
}

new_df = pd.DataFrame(new_data)

# Make predictions for the new data
predictions = clf.predict(new_df[['truck_height', 'truck_width', 'number_of_sensors', 'speed']])

# Find the truck with the highest characteristics and assign truck ID 1
predicted_df = new_df.copy()
predicted_df['truck_id'] = 0
max_characteristics = new_df[['truck_height', 'truck_width', 'number_of_sensors', 'speed']].max(axis=1)
chosen_truck = predicted_df.loc[max_characteristics.idxmax(), 'truck_color']
chosen_truck_id = df.loc[df['truck_color'] == chosen_truck, 'truck_id'].iloc[0]
predicted_df.loc[max_characteristics.idxmax(), 'truck_id'] = chosen_truck_id

# Print the chosen truck from the decision classifier
print(f"Chosen Truck ID: {chosen_truck_id}")
print(f"Chosen Truck Color: {chosen_truck}")

# Constants for the simulation environment
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BORDER_WIDTH = 40

# Constants for the trucks
TRUCK_BODY_WIDTH = 40
TRUCK_BODY_HEIGHT = 60
TRUCK_COLORS = [(255, 0,0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue
TRUCK_SPEED = 2
DISTANCE_BETWEEN_TRUCKS = 150

# Initialize the Pygame module
pygame.init()

# Create the simulation window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Truck Platoon Simulation")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Draw the simulation environment
screen.fill(WHITE)
pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, BORDER_WIDTH))
pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - BORDER_WIDTH, SCREEN_WIDTH, BORDER_WIDTH))
pygame.draw.rect(screen, BLACK, (0, BORDER_WIDTH, BORDER_WIDTH, SCREEN_HEIGHT - 2 * BORDER_WIDTH))
pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - BORDER_WIDTH, BORDER_WIDTH, BORDER_WIDTH, SCREEN_HEIGHT - 2 * BORDER_WIDTH))

# Create trucks
trucks = [
    {
        'id': 0,
        'x': BORDER_WIDTH,                                               # Start from the top-left corner (x-axis)
        'y': BORDER_WIDTH,                                               # Start from the top-left corner (y-axis)
        'dx': TRUCK_SPEED,                                               # Move horizontally (to the right)
        'dy': 0,                                                         # No vertical movement
        'color': TRUCK_COLORS[chosen_truck_id - 3],
        'label': f"ID: 0"
    },
    {
        'id': 1,
        'x': BORDER_WIDTH,                                               # Start from the top-left corner (x-axis)
        'y': BORDER_WIDTH + DISTANCE_BETWEEN_TRUCKS,                      # Start from the top-left corner plus distance (y-axis)
        'dx': TRUCK_SPEED,                                               # Move horizontally (to the right)
        'dy': 0,                                                         # No vertical movement
        'color': TRUCK_COLORS[chosen_truck_id - 2],
        'label': f"ID: 1"
    },
    {
        'id': 2,
        'x': BORDER_WIDTH,                                               # Start from the top-left corner (x-axis)
        'y': BORDER_WIDTH + 2 * DISTANCE_BETWEEN_TRUCKS,                  # Start from the top-left corner plus distance times 2 (y-axis)
        'dx': TRUCK_SPEED,                                               # Move horizontally (to the right)
        'dy': 0,                                                         # No vertical movement
        'color': TRUCK_COLORS[chosen_truck_id - 1],
        'label': f"Lead Truck (ID: {chosen_truck_id})"
    }
]

# Create font for labels
font = pygame.font.Font(None, 24)

# Main simulation loop
running = True
clock = pygame.time.Clock()
while running:
    # Limit the frame rate
    clock.tick(60)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update truck positions
    for truck in trucks:
        truck['x'] += truck['dx']
        truck['y'] += truck['dy']

        # Check boundaries for trucks
        if truck['x'] > SCREEN_WIDTH - BORDER_WIDTH - TRUCK_BODY_WIDTH and truck['dy'] == 0:
            truck['dx'] = 0                                                # Stop horizontal movement
            truck['dy'] = TRUCK_SPEED                                      # Move vertically (downwards)
        elif truck['y'] > SCREEN_HEIGHT - BORDER_WIDTH - TRUCK_BODY_HEIGHT and truck['dx'] == 0:
            truck['dx'] = -TRUCK_SPEED                                     # Move horizontally (to the left)
            truck['dy'] = 0                                                 # No vertical movement
        elif truck['x'] < BORDER_WIDTH and truck['dy'] == 0:
            truck['dx'] = 0                                                 # Stop horizontal movement
            truck['dy'] = -TRUCK_SPEED                                       # Move vertically (upwards)
        elif truck['y'] < BORDER_WIDTH and truck['dx'] == 0:
            truck['dx'] = TRUCK_SPEED                                        # Move horizontally (to the right)
            truck['dy'] = 0                                                  # No vertical movement

    # Draw trucks
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, BORDER_WIDTH))
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - BORDER_WIDTH, SCREEN_WIDTH, BORDER_WIDTH))
    pygame.draw.rect(screen, BLACK, (0, BORDER_WIDTH, BORDER_WIDTH, SCREEN_HEIGHT - 2 * BORDER_WIDTH))
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - BORDER_WIDTH, BORDER_WIDTH, BORDER_WIDTH, SCREEN_HEIGHT - 2 * BORDER_WIDTH))
    
    for truck in trucks:
        pygame.draw.rect(screen, truck['color'], (truck['x'], truck['y'], TRUCK_BODY_WIDTH, TRUCK_BODY_HEIGHT))
        label = font.render(truck['label'], True, BLACK)
        screen.blit(label, (truck['x'], truck['y'] - 20))

    # Update the screen
    pygame.display.flip()

# Quit the simulation
pygame.quit()
