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

    def breathing_exercise(self, time_inhale: int, time_hold: int, time_exhale: int):
        """ Start breathing exercise
        Args:
            time_inhale: a number from 1 to 10 for inhale count
            time_hold: a number from 1 to 10 for hold count
            time_exhale: a number from 1 to 10 for exhale count
        Returns:
            None
        """

        self.furhatClient.speak("Inhale deeply through your nose for " + str(int(time_inhale)) + " seconds.")
        self.furhatClient.gesture_inhale(time_inhale)

        self.furhatClient.speak("Hold your breath for " + str(int(time_hold)) + " seconds.")
        self.furhatClient.gesture_hold(time_hold)

        self.furhatClient.speak("Exhale slowly through your mouth for " + str(int(time_exhale)) + " seconds.")
        self.furhatClient.gesture_exhale(time_exhale)
        return