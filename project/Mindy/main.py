from FurhatClient import FurhatClient
from EmotionDetectionModule import EmotionDetectionModule
from LLMModule import LLMModule
from BreathingGuide import BreathingGuide
from Mood import Mood
import time
import threading

def main():
    # Initialize FurhatClient
    webcam_ready_event = threading.Event()
    done_event = threading.Event()

    furhat_client = FurhatClient()
    furhat_client.init()
    moodDetector = Mood(alpha=0.3) 
    emotion_module = EmotionDetectionModule(webcam_ready_event,done_event, furhat_client, moodDetector)
    emotion_module.init()
    emotion_module.startDetection() 
    
    # Define a breathing pattern and create an instance of BreathingGuide
    breathing_pattern = {"inhale": 4, "hold": 7, "exhale": 8}
    breathing_guide = BreathingGuide(breathing_pattern, furhat_client)

    llmModule = LLMModule(webcam_ready_event,done_event,furhat_client,emotion_module, {},{}, breathing_guide, moodDetector)
    llmModule.start()

    emotion_module.stopDetection() 
if __name__ == "__main__":
    main()
