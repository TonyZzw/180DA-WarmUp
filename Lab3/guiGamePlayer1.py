import paho.mqtt.client as mqtt
import pygame
from pygame.locals import KEYDOWN, K_1, K_2, K_3, K_ESCAPE, K_SPACE

# Initialize Pygame
pygame.init()

# Constants for colors and MQTT settings
WHITE = (255, 255, 255)
PURPLE = (106, 90, 205)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
MQTT_BROKER = 'mqtt.eclipseprojects.io'
SUBSCRIBE_CHANNEL = 'channel1'
PUBLISH_CHANNEL = 'channel2'

# Global variables
opponent_selection = None
user_selection = None
score = 0
output = False
result = None

# Set up the MQTT client
client = mqtt.Client(client_id="player1")

def on_connect(client, userdata, flags, rc):
    client.subscribe(SUBSCRIBE_CHANNEL, qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    global opponent_selection
    opponent_selection = message.payload.decode()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect_async(MQTT_BROKER)
client.loop_start()

# Pygame window setup
screen = pygame.display.set_mode([600, 500])
font = pygame.font.Font('freesansbold.ttf', 32)

def draw_text(message, position, color):
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=position)
    screen.blit(text, text_rect)

def reset_game():
    global user_selection, opponent_selection, selected, output, result
    user_selection = opponent_selection = None
    selected = output = False
    result = None

def update_game_state():
    global score, result, output
    if user_selection == opponent_selection:
        result = "It's a Tie!"
    elif (user_selection, opponent_selection) in [("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")]:
        result = "You Win!"
        score += 1
    else:
        result = "You Lose!"
        score -= 1
    output = True

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    draw_text('1.Rock', (100, 150), BLACK)
    draw_text('2.Paper', (300, 150), BLACK)
    draw_text('3.Scissors', (500, 150), BLACK)

    if user_selection:
        draw_text(f'You selected {user_selection}', (300, 250), PURPLE)
        client.publish(PUBLISH_CHANNEL, user_selection)

    if user_selection and opponent_selection and not output:
        update_game_state()

  # Declare global inside the loop
    if output and result is not None:
        draw_text(result, (300, 400), PURPLE)
        draw_text(f'Score: {score}', (450, 450), BLUE)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE:
                reset_game()
            elif event.key in [K_1, K_2, K_3]:
                user_selection = ["rock", "paper", "scissors"][event.key - K_1]

    pygame.display.update()

# Cleanup
client.loop_stop()
client.disconnect()
pygame.quit()

