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

    def breathing_exercise(self, time_inhale: int, time_hold: int, time_exhale: int, repeat: int):
        """ Start breathing exercise
        Args:
            time_inhale: a number from 1 to 10 for inhale count
            time_hold: a number from 1 to 10 for hold count
            time_exhale: a number from 1 to 10 for exhale count
            repeat: number of time to repeat the exercise
        Returns:
            None
        """
        self.furhatClient.speak("Lets start a"+ str(int(time_inhale)) +" "+str(int(time_hold))+" "+str(int(time_exhale))+ "breathing exercise for "+str(int(repeat))+"times")
        for i in range(int(repeat)):
            self.furhatClient.speak("Inhale")
            self.furhatClient.gesture_inhale(time_inhale)

            self.furhatClient.speak("Hold")
            self.furhatClient.gesture_hold(time_hold)

            self.furhatClient.speak("Exhale")
            self.furhatClient.gesture_exhale(time_exhale)
        return
