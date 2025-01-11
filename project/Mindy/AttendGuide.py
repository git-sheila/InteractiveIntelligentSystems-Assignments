from FurhatClient import FurhatClient
#from EmotionDetectionModule import EmotionDetectionModule

class AttendGuide:
    def __init__(self, furhatClient: FurhatClient):
        """Constructor: Initializes AttendGuide and FurhatClient."""
        print("Initializing AttendGuide...")
        self.furhatClient = furhatClient
        #self.emotionModule = emotionModule

    def __del__(self):
        """Destructor: Cleans up AttendGuide"""
        print("Destroying AttendGuide...")

    def start(self):
        """Starts guiding the breathing exercise using FurhatClient."""
        #inhale = self.pattern.get('inhale', 3)
        #exhale = self.pattern.get('exhale', 3)
        #hold = self.pattern.get('hold', 2)
        
        self.furhatClient.speak("Starting attend guide...")
        #print(f"Inhale for {inhale} seconds, hold for {hold} seconds, exhale for {exhale} seconds.")

    def attend_user(self,loca: str):
        #loca = self.emotionModule.fetchLocation()
        print("The location in the AttendGuide is " + str(loca) + "*************************************************")
        #loca=str("5,15,0")
        self.furhatClient.attendLocation(loca)



