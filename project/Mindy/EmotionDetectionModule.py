import threading
import time

import cv2
import joblib
import tempfile
from feat import Detector
from sklearn.preprocessing import StandardScaler
from FurhatClient import FurhatClient
from Mood import Mood

class EmotionDetectionModule:
    def __init__(self, webcam_ready_event, done_event, furhatClient: FurhatClient, moodDetector: Mood):
        """
        Constructor: Initializes EmotionDetectionModule
        :param webcam_ready_event: threading.Event to signal webcam readiness
        :param done_event: threading.Event to signal when to stop detection
        """
        self.webcam_ready_event = webcam_ready_event
        self.done_event = done_event
        self._is_detecting = False
        self._detection_thread = None
        self.stable_emotion = None
        self.location_coordinates = None
        self.furhatClient = furhatClient
        self.moodDetector = moodDetector

        # Load trained models
        self.valence_model = joblib.load("valence_model.pkl")
        self.arousal_model = joblib.load("arousal_model.pkl")
        self.emotion_model = joblib.load("best_random_forest_model.pkl")

        # Initialize the detector
        self.detector = Detector(device="cuda")

        # StandardScaler for feature scaling (if required)
        self.scaler = StandardScaler()

        # Emotion mapping
        self.emotion_mapping = {
            0: "neutral",
            1: "happy",
            2: "sad",
            3: "surprise",
            4: "fear",
            5: "disgust",
            6: "anger"
        }

    def __del__(self):
        """ Destructor: Cleans up and stops the emotion detection thread """
        print("Destroying EmotionDetectionModule...")
        self.stopDetection()

    def init(self):
        """ Initializes detection settings """
        print("Emotion Detection Module initialized.")

    def _detect_emotions(self):
        """ Private method: Detect emotions continuously in a thread. """
        while self._is_detecting:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error: Could not open video.")
                return
            last_emotion = None
            
            emotion_stability_count = 0  # Tracks stability of emotion
            self.webcam_ready_event.set()
            while not self.done_event.is_set():
                # Capture frame-by-frame
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame.")
                    break

                try:
                    faces = self.detector.detect_faces(frame)
                    #faces = faces[0]

                    # Process first detected face for simplicity
                    if len(faces[0]) > 0:
                        #gaze calcs
                        updown,leftright,temp = frame.shape
                        x_min, y_min, x_max, y_max, confidence = faces[0][0]

                        # Calculate center coordinates
                        x_center = (x_min + x_max) / 2
                        y_center = (y_min + y_max) / 2
                        x_coordinate = round((leftright/2-x_center), 2)
                        y_coordinate = round((updown/2-y_center), 2)
                        #set gaze
                        self.location_coordinates = "{:.2f},{:.2f},2".format(1*x_coordinate/leftright, 1*y_coordinate/updown)
                        #gaze done
                        self.furhatClient.attendLocation(self.location_coordinates)
                        
                        landmarks = self.detector.detect_landmarks(frame, faces)
                        aus = self.detector.detect_aus(frame, landmarks)

                        features = aus[0][0]

                        # Predict valence and arousal
                        predicted_valence = round(self.valence_model.predict([features])[0], 2)
                        predicted_arousal = round(self.arousal_model.predict([features])[0], 2)

                        # Combine AUs with predicted valence and arousal for emotion classification
                        augmented_features = list(features) + [predicted_valence, predicted_arousal] #notun 22 

                        # Predict emotion (as digit) and map to string
                        predicted_emotion_digit = self.emotion_model.predict([augmented_features])[0]
                        predicted_emotion = self.emotion_mapping.get(predicted_emotion_digit, "unknown")
                        
                        # Track emotion stability
                        if predicted_emotion == last_emotion:
                            emotion_stability_count += 1
                            print(f"Predicted emotion:{predicted_emotion}"+f" Count :{emotion_stability_count}")
                            if emotion_stability_count >= 3:  # Stable emotion threshold
                                self.moodDetector.update_emotion(self.stable_emotion)
                                print("updateMood")
                                emotion_stability_count = 0
                                if self.stable_emotion is None or predicted_emotion != self.stable_emotion:
                                    self.stable_emotion = predicted_emotion
                                    print(f"Stable emotion detected: {self.stable_emotion}")
                                    
                        else:
                            print (f" Predicted {predicted_emotion} and last emotion {last_emotion}")
                            emotion_stability_count = 0  # Reset counter if emotion changes
                        last_emotion = predicted_emotion
                    else:
                        print (" No face detected")
                except Exception as e:
                    print(f"Exception in Emotion Detection : {e}")
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
            return "neutral"
    
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
