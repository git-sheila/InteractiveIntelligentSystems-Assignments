import threading
import time

class EmotionDetectionModule:
    def __init__(self):
        """Constructor: Initializes EmotionDetectionModule"""
        print("Initializing EmotionDetectionModule...")
        self.emotions_detected = []
        self._is_detecting = False
        self._detection_thread = None

    def __del__(self):
        """Destructor: Cleans up and stops the emotion detection thread"""
        print("Destroying EmotionDetectionModule...")
        self.stopConversation()

    def init(self):
        """Initializes detection settings"""
        print("Emotion Detection Module initialized.")

    def _detect_emotions(self):
        """Private method: Simulates continuous emotion detection in a thread."""
        while self._is_detecting:
            # Simulate emotion detection by cycling through dummy emotions
            detected_emotion = ["happy", "sad", "neutral"]
            current_emotion = detected_emotion[time.time_ns() % 3]
            self.emotions_detected.append(current_emotion)
            print(f"Detected emotion: {current_emotion}")
            time.sleep(2)  # Simulate detection interval

    def startDetection(self):
        """Starts the emotion detection process in a separate thread."""
        if not self._is_detecting:
            print("Starting continuous emotion detection...")
            self._is_detecting = True
            self._detection_thread = threading.Thread(target=self._detect_emotions, daemon=True)
            self._detection_thread.start()
        else:
            print("Emotion detection is already running.")

    def fetchFullDetectionList(self) -> list:
        """Returns the full list of detected emotions."""
        print("Fetching full detection list...")
        return self.emotions_detected

    def startConversation(self):
        """Simulates starting a conversation for emotion detection."""
        print("Conversation started for emotion detection.")

    def stopConversation(self) -> str:
        """
        Stops the detection thread and returns the final detected emotion.
        If no emotions were detected, it returns 'neutral' by default.
        """
        if self._is_detecting:
            print("Stopping emotion detection...")
            self._is_detecting = False
            if self._detection_thread:
                self._detection_thread.join()
            print("Emotion detection stopped.")
        else:
            print("Emotion detection was not running.")
        
        detected_emotion = self.emotions_detected[-1] if self.emotions_detected else "neutral"
        print(f"Final detected emotion: {detected_emotion}")
        return detected_emotion
