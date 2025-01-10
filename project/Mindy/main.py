from FurhatClient import FurhatClient
from EmotionDetectionModule import EmotionDetectionModule
from FileHandler import FileHandler
from LLMModule import LLMModule
from BreathingGuide import BreathingGuide
import time
import threading

def main():
    # Initialize FurhatClient
    webcam_ready_event = threading.Event()
    done_event = threading.Event()

    emotion_module = EmotionDetectionModule(webcam_ready_event,done_event)
    emotion_module.init()
    emotion_module.startDetection() 
    
    furhat_client = FurhatClient()
    furhat_client.init()

    # Define a breathing pattern and create an instance of BreathingGuide
    breathing_pattern = {"inhale": 4, "hold": 7, "exhale": 8}
    breathing_guide = BreathingGuide(breathing_pattern, furhat_client)

    llmModule = LLMModule(furhat_client,emotion_module, {},{}, breathing_guide)
    llmModule.start()

    emotion_module.stopDetection() 
if __name__ == "__main__":
    main()
