import threading
import queue
import cv2
from furhat_remote_api import FurhatRemoteAPI
from feat import Detector
from feat.utils import FEAT_EMOTION_COLUMNS
from PIL import Image as PILImage
from IPython.display import Image

# Function for Furhat API operations
def furhat_interaction(emotion_queue, webcam_ready_event):
    furhat = FurhatRemoteAPI("localhost")
    furhat.set_voice(name='Anna')  # Replace 'Anna' with your desired female voice
    webcam_ready_event.wait()
    while True:
        # Check if there's a new emotion detected
        if not emotion_queue.empty():
            emotion = emotion_queue.get()
            print(f"Detected emotion: {emotion}")
            # Respond to emotion
            furhat.say(text=f"I see that you're feeling {emotion}. Let's talk about it!")

        # Ask the user something and listen
        furhat.say(text="How are you doing today?")
        print("Listening to user...")
        result = furhat.listen()
        if result:
            print("You said:", result['text'])
        else:
            print("No speech detected!")

# Function for emotion detection
def emotion_detection(emotion_queue, webcam_ready_event):
    face_tracker = cv2.CascadeClassifier("frontal_face_features.xml")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    recording = False
    last_emotion = None
    stable_emotion = None
    emotion_stability_count = 0  # Tracks stability of emotion
    detector = Detector(device="cuda")
    webcam_ready_event.set()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        #print(frame)
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

            # Check stability
            if current_emotion == last_emotion:
                stability_counter += 1
                if stability_counter >= 4:
                    if stable_emotion is None or current_emotion != stable_emotion:
                        stable_emotion = current_emotion
                        emotion_queue.put(stable_emotion)  # Share stable emotion with Furhat thread
                        print(f"Stable emotion detected: {stable_emotion}")
            else:
                stability_counter = 0  # Reset counter if emotion changes

            last_emotion = current_emotion 

    cap.release()
    cv2.destroyAllWindows()

# Main function
def main():
    emotion_queue = queue.Queue()  # Shared queue for communication
    webcam_ready_event = threading.Event()

    # Create threads
    furhat_thread = threading.Thread(target=furhat_interaction, args=(emotion_queue,webcam_ready_event))
    camera_thread = threading.Thread(target=emotion_detection, args=(emotion_queue,webcam_ready_event))

    # Start threads
    furhat_thread.start()
    camera_thread.start()

    # Wait for threads to complete (optional, but good for cleanup)
    furhat_thread.join()
    camera_thread.join()

if __name__ == "__main__":
    main()
