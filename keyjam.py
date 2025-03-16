import random
import string
from pynput import keyboard

# Create a set of all possible characters
all_characters = set(string.ascii_letters + string.digits + string.punctuation + ' ')

# Function to get a random character that is not the same as the input character
def get_random_character(exclude):
    while True:
        random_char = random.choice(list(all_characters))
        if random_char != exclude:
            return random_char

# Create a keyboard controller
controller = keyboard.Controller()

# Function to handle key press events
def on_press(key):
    try:
        # Check if the key has a character representation
        if hasattr(key, 'char') and key.char is not None:
            # Get a random character that is not the same as the pressed key
            new_char = get_random_character(key.char)
            print(f"Swapping '{key.char}' with '{new_char}'")
            # Simulate the new character input
            controller.press(new_char)  # Press the new character
            controller.release(new_char)  # Release the new character
    except AttributeError:
        pass  # Handle special keys if necessary

# Start listening to keyboard events
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Keep the script running
listener.join()
