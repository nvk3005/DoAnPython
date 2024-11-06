import pyautogui
import time

print("Press Ctrl+C to stop.")

try:
    while True:
        # Get the current mouse position
        x, y = pyautogui.position()
        print(f"Mouse position: (X: {x}, Y: {y})", end="\r")
        time.sleep(0.1)  # Update every 0.1 seconds
except KeyboardInterrupt:
    print("\nStopped.")
