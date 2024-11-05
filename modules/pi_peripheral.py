import RPi.GPIO as GPIO
def led_blink(duration=1):
    # Set up GPIO mode
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Define pins
    LED_PIN = 8
    # Setup pins as outputs
    GPIO.setup(LED_PIN, GPIO.OUT)
    """Blink the LED once"""
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(duration)

def single_beep(duration=0.5):
    # Set up GPIO mode
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    """Make the buzzer beep once"""
    BUZZER_PIN = 23
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(duration)