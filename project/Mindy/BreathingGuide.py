from FurhatClient import FurhatClient

class BreathingGuide:
    def __init__(self, pattern: dict, furhatClient: FurhatClient):
        """Constructor: Initializes BreathingGuide with breathing pattern and FurhatClient."""
        print("Initializing BreathingGuide...")
        self.pattern = pattern
        self.furhatClient = furhatClient

    def __del__(self):
        """Destructor: Cleans up BreathingGuide"""
        print("Destroying BreathingGuide...")

    def start(self):
        """Starts guiding the breathing exercise using FurhatClient."""
        inhale = self.pattern.get('inhale', 3)
        exhale = self.pattern.get('exhale', 3)
        hold = self.pattern.get('hold', 2)
        
        self.furhatClient.speak("Starting breathing guide...")
        print(f"Inhale for {inhale} seconds, hold for {hold} seconds, exhale for {exhale} seconds.")

    def temp_exercise(self):
        self.furhatClient.speak("Temporary exercise is going on")

    def breathing_exercise(self):
        self.furhatClient.speak("Inhale deeply through your nose for 4 seconds.")
        self.furhatClient.gesture_inhale(4)

        self.furhatClient.speak("Hold your breath for 4 seconds.")
        self.furhatClient.gesture_hold(4)

        self.furhatClient.speak("Exhale slowly through your mouth for 4 seconds.")
        #Gesture to breathe out
        self.furhatClient.gesture_exhale(4)