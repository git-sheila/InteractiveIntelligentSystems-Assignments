import threading
import queue
import cv2
from furhat_remote_api import FurhatRemoteAPI
from feat import Detector
from feat.utils import FEAT_EMOTION_COLUMNS
from PIL import Image as PILImage
from IPython.display import Image
import csv
from datetime import datetime

# Function to ask questions using Furhat and save user responses to a CSV file
def ask_questions_and_save_responses(furhat, csv_file, fieldnames):
    """
    Function to ask questions using Furhat and save user responses to a CSV file.
    """
    # List of questions
    questions = [
        "Welcome to the Mindspace Clinic . How can I assist you today?",
        "Is this your first visit to our clinic?",
        "What is your name?",
        "Welcome, {name}! Since it’s your first visit, I’d like to ask a few questions to help us better assist. How are you feeling today?",
        "What symptoms have you been experiencing?",
        "How often do you experience these symptoms?",
        "Is there a specific time or situation when you feel more anxious or stressed?",
        "Have you ever tried mindfulness or relaxation techniques before?",
        "Are you currently on any medication for anxiety or stress?",
        "Understood. One last question: Have you been experiencing difficulty sleeping lately?",
        "Thank you for sharing all of this! I would like to suggest Dr. Emily for you; however, you are welcome to choose other doctors.",
        "This information will be helpful for Dr. Emily. Before your session, would you like me to guide you through a short breathing exercise to help ease some of the anxiety?",
        "Alright, let’s begin. Please sit comfortably and close your eyes. Take a deep breath in through your nose for four counts... hold it for four counts... and exhale slowly through your mouth for four counts. Let’s repeat this three more times. Let me know how you’re feeling after.",
        "Dr. Emily is available next at 10:30 AM tomorrow morning. Would that be a suitable appointment time for you?",
        "You’re welcome, {name}. It was a pleasure assisting you today. Take care, and I hope the session helps you feel even better."
    ]

    # Initialize name for personalized questions
    name = ""

    for question in questions:
        # Personalize the question if it contains {name}
#        if "{name}" in question and name:
#            question = question.replace("{name}", name)
        
        # Furhat asks the question
        furhat.say(text=question, blocking=True)
        print(question)

        # Furhat listens for a response
        print ("RESPONSE")
        response = furhat.listen()
        print(response)

        # Save the name if the question asks for it
        if "What is your name?" in question:
            name = response  # Save the name for personalized follow-ups
            print("NAME IS -")
            print(name)

        # Save the response to CSV
        with open(csv_file, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({"Timestamp": datetime.now(), "Question": question, "Answer": response})

# Function for Furhat API operations
def furhat_interaction(emotion_queue, webcam_ready_event, done_event):
    furhat = FurhatRemoteAPI("localhost")
    furhat.set_voice(name='Anna')  # Replace 'Anna' with your desired female voice
    webcam_ready_event.wait()
    #while True:
        # Check if there's a new emotion detected
    if not emotion_queue.empty():
        emotion = emotion_queue.get()
        print("Detected emotion: {emotion}")
        # Respond to emotion
        furhat.say(text=f"I see that you're feeling {emotion}. Let's talk about it!")

    # Ask the user something and listen
    furhat.say(text="How are you doing today?")
    print("Listening to user...")
    result = furhat.listen()
    if result:
        print("You said:", result)
        # Call the function to ask questions and save responses
        ask_questions_and_save_responses(furhat, 'user_responses.csv', ['Timestamp', 'Question', 'Answer'])
        done_event.set()
    else:
        print("No speech detected!")

# Function for emotion detection
def emotion_detection(emotion_queue, webcam_ready_event, done_event):
    face_tracker = cv2.CascadeClassifier("frontal_face_features.xml")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    recording = False
    last_emotion = None
    stable_emotion = None
    emotion_stability_count = 0  # Tracks stability of emotion
    detector = Detector(device="cpu")
    webcam_ready_event.set()
    while not done_event.is_set():
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
            print("**In emotion detection")
            print("Current emotion:", current_emotion)
            # Check stability
            if current_emotion == last_emotion:
                emotion_stability_count += 1
                if emotion_stability_count >= 4:
                    if stable_emotion is None or current_emotion != stable_emotion:
                        stable_emotion = current_emotion
                        emotion_queue.put(stable_emotion)  # Share stable emotion with Furhat thread
                        print("Stable emotion detected: {stable_emotion}")
            else:
                emotion_stability_count = 0  # Reset counter if emotion changes

            last_emotion = current_emotion

    cap.release()
    cv2.destroyAllWindows()

# Main function
def main():
    emotion_queue = queue.Queue()  # Shared queue for communication
    webcam_ready_event = threading.Event()
    done_event = threading.Event()

    # Create threads
    furhat_thread = threading.Thread(target=furhat_interaction, args=(emotion_queue,webcam_ready_event, done_event))
    camera_thread = threading.Thread(target=emotion_detection, args=(emotion_queue,webcam_ready_event, done_event))

    # Start threads
    furhat_thread.start()
    camera_thread.start()

    # Wait for threads to complete (optional, but good for cleanup)
    furhat_thread.join()
    camera_thread.join()

if __name__ == "__main__":
    main()
