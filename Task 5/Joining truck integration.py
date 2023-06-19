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
    'truck_height': [16, 19, 20],
    'truck_width': [24, 18, 20],
    'number_of_sensors': [18, 20, 21],
    'speed': [170, 198, 180]
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
TRUCK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue
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
def draw_environment():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, BORDER_WIDTH))
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - BORDER_WIDTH, SCREEN_WIDTH, BORDER_WIDTH))
    pygame.draw.rect(screen, BLACK, (0, BORDER_WIDTH, BORDER_WIDTH, SCREEN_HEIGHT - 2 * BORDER_WIDTH))
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - BORDER_WIDTH, BORDER_WIDTH, BORDER_WIDTH, SCREEN_HEIGHT - 2 * BORDER_WIDTH))

# Create trucks
trucks = [
    {
        'id': 0,
        'x': SCREEN_WIDTH // 1.2 - TRUCK_BODY_WIDTH // 0.40,
        'y': SCREEN_HEIGHT // 2 - TRUCK_BODY_HEIGHT // 2 - DISTANCE_BETWEEN_TRUCKS,
        'dx': TRUCK_SPEED,
        'dy': 0,
        'color': TRUCK_COLORS[chosen_truck_id - 3],
        'label': 'Truck 1',
        'joined': False
    }, 
    {
        'id': 1,
        'x': SCREEN_WIDTH // 1.2 - TRUCK_BODY_WIDTH // 2,
        'y': SCREEN_HEIGHT // 2 - TRUCK_BODY_HEIGHT // 2 - DISTANCE_BETWEEN_TRUCKS,
        'dx': TRUCK_SPEED,
        'dy': 0,
        'color': TRUCK_COLORS[chosen_truck_id - 2],
        'label': 'Truck 2',
        'joined': False
    },
    {
        'id': 2,
        'x': SCREEN_WIDTH // 1.2 - TRUCK_BODY_WIDTH // 2,
        'y': SCREEN_HEIGHT // 3 - TRUCK_BODY_HEIGHT // 50,
        'dx': TRUCK_SPEED,
        'dy': 0,
        'color': TRUCK_COLORS[chosen_truck_id - 1],
        'label': f"Lead Truck (ID: {chosen_truck_id})",
        'joined': False
    }
]

# Create font for labels
font = pygame.font.Font(None, 24)

# Variables for tracking truck joining
truck_3_started = False
truck_2_joined = False
truck_1_joined = False

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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not truck_3_started:
                truck_3_started = True
            elif truck_3_started and not truck_2_joined:
                truck_2_joined = True
            elif truck_2_joined and not truck_1_joined:
                truck_1_joined = True

    # Update truck positions
    for truck in trucks:
        if truck['id'] == 2 and truck_3_started:
            truck['x'] += truck['dx']
            truck['y'] += truck['dy']

            # Check boundaries for truck 3
            if truck['x'] >= SCREEN_WIDTH - BORDER_WIDTH - TRUCK_BODY_WIDTH and truck['dy'] == 0:
                truck['dx'] = 0
                truck['dy'] = TRUCK_SPEED
            elif truck['y'] >= SCREEN_HEIGHT - BORDER_WIDTH - TRUCK_BODY_HEIGHT and truck['dx'] == 0:
                truck['dx'] = -TRUCK_SPEED
                truck['dy'] = 0
            elif truck['x'] <= BORDER_WIDTH and truck['dy'] == 0:
                truck['dx'] = 0
                truck['dy'] = -TRUCK_SPEED
            elif truck['y'] <= BORDER_WIDTH and truck['dx'] == 0:
                truck['dx'] = TRUCK_SPEED
                truck['dy'] = 0

            # Ensure truck 3 stays within the boundaries
            if truck['x'] >= SCREEN_WIDTH - BORDER_WIDTH - TRUCK_BODY_WIDTH and truck['dy'] == 0:
                truck['x'] = SCREEN_WIDTH - BORDER_WIDTH - TRUCK_BODY_WIDTH
            elif truck['y'] >= SCREEN_HEIGHT - BORDER_WIDTH - TRUCK_BODY_HEIGHT and truck['dx'] == 0:
                truck['y'] = SCREEN_HEIGHT - BORDER_WIDTH - TRUCK_BODY_HEIGHT
            elif truck['x'] <= BORDER_WIDTH and truck['dy'] == 0:
                truck['x'] = BORDER_WIDTH
            elif truck['y'] <= BORDER_WIDTH and truck['dx'] == 0:
                truck['y'] = BORDER_WIDTH

        if truck['id'] == 1 and truck_2_joined:
            truck['x'] += truck['dx']
            truck['y'] += truck['dy']

            # Check boundaries for truck 2
            if truck['x'] >= SCREEN_WIDTH - BORDER_WIDTH - TRUCK_BODY_WIDTH and truck['dy'] == 0:
                truck['dx'] = 0
                truck['dy'] = TRUCK_SPEED
            elif truck['y'] >= SCREEN_HEIGHT - BORDER_WIDTH - TRUCK_BODY_HEIGHT and truck['dx'] == 0:
                truck['dx'] = -TRUCK_SPEED
                truck['dy'] = 0
            elif truck['x'] <= BORDER_WIDTH and truck['dy'] == 0:
                truck['dx'] = 0
                truck['dy'] = -TRUCK_SPEED
            elif truck['y'] <= BORDER_WIDTH and truck['dx'] == 0:
                truck['dx'] = TRUCK_SPEED
                truck['dy'] = 0

        if truck['id'] == 0 and truck_1_joined:
            truck['x'] += truck['dx']
            truck['y'] += truck['dy']

            # Check boundaries for truck 1
            if truck['x'] >= SCREEN_WIDTH - BORDER_WIDTH - TRUCK_BODY_WIDTH and truck['dy'] == 0:
                truck['dx'] = 0
                truck['dy'] = TRUCK_SPEED
            elif truck['y'] >= SCREEN_HEIGHT - BORDER_WIDTH - TRUCK_BODY_HEIGHT and truck['dx'] == 0:
                truck['dx'] = -TRUCK_SPEED
                truck['dy'] = 0
            elif truck['x'] <= BORDER_WIDTH and truck['dy'] == 0:
                truck['dx'] = 0
                truck['dy'] = -TRUCK_SPEED
            elif truck['y'] <= BORDER_WIDTH and truck['dx'] == 0:
                truck['dx'] = TRUCK_SPEED
                truck['dy'] = 0

    # Draw the environment and trucks
    draw_environment()
    for truck in trucks:
        pygame.draw.rect(screen, truck['color'], (truck['x'], truck['y'], TRUCK_BODY_WIDTH, TRUCK_BODY_HEIGHT))
        label = font.render(truck['label'], True, BLACK)
        screen.blit(label, (truck['x'], truck['y'] - 20))

    # Update the display
    pygame.display.flip()

# Quit the simulation
pygame.quit()
