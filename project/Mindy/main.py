from FurhatClient import FurhatClient
from EmotionDetectionModule import EmotionDetectionModule
from FileHandler import FileHandler
from LLMModule import LLMModule
from BreathingGuide import BreathingGuide
import time

def main():
    # Initialize FurhatClient
    furhat_client = FurhatClient()
    furhat_client.init()
    
    # Speak and listen example
    furhat_client.speak("Hello! How can I assist you today?")
    user_response = furhat_client.listen()
    response = furhat_client.getResponse(user_response)
    furhat_client.speak(response)

    # Initialize EmotionDetectionModule and start detection thread
    emotion_module = EmotionDetectionModule()
    emotion_module.init()
    emotion_module.startDetection()  # Start detection in a separate thread

    # Simulate running the detection process indefinitely (or until user stops it)
    print("Emotion detection is running in the background. Press Ctrl+C to stop.")
    try:
        for _ in range(5):  # Simulate 10 seconds of main program running
            time.sleep(2)
            emotions = emotion_module.fetchFullDetectionList()
            print(f"Current detected emotions: {emotions}")
    except KeyboardInterrupt:
        print("Main program interrupted. Stopping detection...")

    # Stop conversation and get final emotion
    final_emotion = emotion_module.stopConversation()
    print(f"Final detected emotion: {final_emotion}")

    # File handling example
    file_handler = FileHandler()
    file_name = "data.txt"
    data_to_write = f"User response: {user_response}, Emotion detected: {final_emotion}"
    file_handler.writeData(file_name, data_to_write)
    read_data = file_handler.readData(file_name)
    print(f"Data from file: {read_data}")

    # Initialize LLMModule
    user_data = {"name": "John Doe", "age": 30}
    doctor_info = {"doctor_name": "Dr. Smith", "specialization": "Cardiology"}
    llm_module = LLMModule(furhat_client, user_data, doctor_info)
    llm_module.start()

    # Initialize BreathingGuide
    breathing_pattern = {"inhale": 4, "hold": 3, "exhale": 4}
    breathing_guide = BreathingGuide(breathing_pattern, furhat_client)
    breathing_guide.start()

if __name__ == "__main__":
    main()
