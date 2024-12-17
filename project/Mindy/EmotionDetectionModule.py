class EmotionDetectionModule:
    def __init__(self):
        """Constructor: Initializes EmotionDetectionModule"""
        print("Initializing EmotionDetectionModule...")
        self.emotions_detected = []

    def __del__(self):
        """Destructor: Cleans up EmotionDetectionModule"""
        print("Destroying EmotionDetectionModule...")

    def init(self):
        """Initializes detection settings"""
        print("Emotion Detection Module initialized.")

    def startDetection(self):
        """Starts the emotion detection process."""
        print("Emotion detection started...")

    def fetchFullDetectionList(self) -> list:
        """Returns the full list of detected emotions."""
        print("Fetching full detection list...")
        self.emotions_detected = ["happy", "sad", "neutral"]  # Simulated data
        return self.emotions_detected

    def startConversation(self):
        """Simulates starting a conversation for emotion detection."""
        print("Conversation started for emotion detection.")

    def stopConversation(self) -> str:
        """Stops the conversation and returns the final detected emotion."""
        detected_emotion = "neutral"  # Simulated final emotion
        print(f"Conversation stopped. Final detected emotion: {detected_emotion}")
        return detected_emotion
