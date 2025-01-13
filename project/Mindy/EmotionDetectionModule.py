import threading
import time

import cv2
#from furhat_remote_api import FurhatRemoteAPI
from feat import Detector
from feat.utils import FEAT_EMOTION_COLUMNS
from PIL import Image as PILImage
from FurhatClient import FurhatClient


class EmotionDetectionModule:
    def __init__(self, webcam_ready_event, done_event, furhatClient: FurhatClient):
        """
        Constructor: Initializes EmotionDetectionModule
        :param webcam_ready_event: threading.Event to signal webcam readiness
        :param done_event: threading.Event to signal when to stop detection
        """
        self.webcam_ready_event = webcam_ready_event
        self.done_event = done_event
        self.emotions_detected = []
        self._is_detecting = False
        self._detection_thread = None
        self.stable_emotion = None
        self.location_coordinates = None
        self.furhatClient = furhatClient

    def __del__(self):
        """ Destructor: Cleans up and stops the emotion detection thread """
        print("Destroying EmotionDetectionModule...")
        self.stopDetection()
        self.stopConversation()

    def init(self):
        """ Initializes detection settings """
        print("Emotion Detection Module initialized.")

    def _detect_emotions(self):
        """ Private method: Simulates continuous emotion detection in a thread. """
        while self._is_detecting:
            face_tracker = cv2.CascadeClassifier("frontal_face_features.xml")
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error: Could not open video.")
                return
            detector = Detector(device="cuda")
            last_emotion = None
            
            emotion_stability_count = 0  # Tracks stability of emotion
            self.webcam_ready_event.set()
            while not self.done_event.is_set():
                # Capture frame-by-frame
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame.")
                    break
                faces = detector.detect_faces(frame)
                landmarks = detector.detect_landmarks(frame, faces)
                emotions = detector.detect_emotions(frame, faces, landmarks)
                faces = faces[0]
                landmarks = landmarks[0]
                emotions = emotions[0]
                # Process first detected face for simplicity
                if len(faces) > 0:
                    strongest_emotion = emotions.argmax(axis=1)[0]  # Get the strongest emotion
                    current_emotion = FEAT_EMOTION_COLUMNS[strongest_emotion]
                    updown,leftright,temp = frame.shape
                    x_min, y_min, x_max, y_max, confidence = faces[0]

                    # Calculate center coordinates
                    x_center = (x_min + x_max) / 2
                    y_center = (y_min + y_max) / 2
                    x_coordinate = round((leftright/2-x_center), 2)
                    y_coordinate = round((updown/2-y_center), 2)
                    #set gaze
                    self.location_coordinates = "{:.2f},{:.2f},2".format(1*x_coordinate/leftright, 1*y_coordinate/updown)

                    self.furhatClient.attendLocation(self.location_coordinates)
                    print("Current emotion:", current_emotion)
                    # Check stability
                    if current_emotion == last_emotion:
                        emotion_stability_count += 1
                        if emotion_stability_count >= 4:
                            if self.stable_emotion is None or current_emotion != self.stable_emotion:
                                self.stable_emotion = current_emotion
                                print("Stable emotion detected: {self.stable_emotion}")
                                self.emotions_detected.append(current_emotion)
                    else:
                        emotion_stability_count = 0  # Reset counter if emotion changes
                    last_emotion = current_emotion
                
            print("**Emotion detection stopping")
            cap.release()
            cv2.destroyAllWindows()
        
    def startDetection(self):
        """ Starts the emotion detection process in a separate thread. """
        if not self._is_detecting:
            print("Starting continuous emotion detection...")
            self._is_detecting = True
            self._detection_thread = threading.Thread(target=self._detect_emotions, daemon=True)
            self._detection_thread.start()
        else:
            print("Emotion detection is already running.")

    def fetchCurrentEmotion(self) -> str:
        if self.stable_emotion:
            return self.stable_emotion
        else:
            return ""
    
    def fetchLocation(self) -> str:
        if self.location_coordinates:
            return self.location_coordinates
        else:
            return "0,0,0"
        
    def stopDetection(self):
        """ Stops the detection thread and returns the final detected emotion."""
        if self._is_detecting:
            print("Stopping emotion detection...")
            self._is_detecting = False
            self.done_event.set()
            if self._detection_thread:
                self._detection_thread.join()
            print("Emotion detection stopped.")
        else:
            print("Emotion detection was not running.")

    def fetchFullDetectionList(self) -> list:
        """ Returns the full list of detected emotions. """
        print("Fetching full detection list...")
        return self.emotions_detected

    def startConversation(self):
        """ For conversations, emotions during a conversation , this function should help as a starting point """
        print("Conversation started for emotion detection.")

    def stopConversation(self) -> str:
        """ If no emotions were detected, it returns 'neutral' by default."""
        detected_emotion = self.emotions_detected[-1] if self.emotions_detected else "neutral"
        print(f"Final detected emotion: {detected_emotion}")
        return detected_emotion