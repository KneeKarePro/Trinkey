import rotaryio
import digitalio
import board
import neopixel

def position_to_color(position):
    """Map position to a color."""

    if position < 34:  # Red to Orange
        # Linear interpolation between red (255,0,0) to orange (255,165,0)
        green = round(165 * (position / 34))
        return (255, green, 0)
    
    elif position < 68:  # Orange to Yellow
        # Linear interpolation between orange (255,165,0) to yellow (255,255,0)
        green = 165 + round((255 - 165) * ((position - 34) / 34))
        return (255, green, 0)
    
    elif position < 101:  # Yellow to Green
        # Linear interpolation between yellow (255,255,0) to green (0,255,0)
        red = 255 - round(255 * ((position - 68) / 33))
        return (red, 255, 0)
    
    else:  # Green to White
        # Linear interpolation between green (0,255,0) to white (255,255,255)
        increment = round(255 * ((position - 101) / 34))
        return (increment, 255, increment)

print("Welcome to KneeKare Pro")

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.5)
encoder = rotaryio.IncrementalEncoder(board.ROTA, board.ROTB)
switch = digitalio.DigitalInOut(board.SWITCH)
switch.switch_to_input(pull=digitalio.Pull.DOWN)

last_position = None
while True:
    position = encoder.position % 136  # Limit position from 0 to 135

    if last_position is None or position != last_position:
        print("Current position: " + str(position))

        if not switch.value:
            # Change the color based on position
            pixel.fill(position_to_color(position))
            
        else:
            # Change the brightness
            if position > last_position:  # Increase
                pixel.brightness = min(1.0, pixel.brightness + 0.1)
            else:  # Decrease
                pixel.brightness = max(0, pixel.brightness - 0.1)
    last_position = position
