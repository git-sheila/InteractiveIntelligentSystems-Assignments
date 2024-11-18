import cv2
import os
import numpy as np
#import opencv_jupyter_ui as jcv2
from feat import Detector
from IPython.display import Image
from PIL import Image as PILImage
from feat.utils import FEAT_EMOTION_COLUMNS
import csv
import pandas as pd

detector = Detector(device="cpu")

output_file = "output.csv"
au_columns = [f"AU{str(i).zfill(2)}" for i in range(20)]

for file_name in os.listdir("freepik_dataset/dataset/images"):
    file_path = os.path.join("freepik_dataset/dataset/images", file_name)
    image = cv2.imread(file_path)
    
    if image is not None:
        print(file_path)
        faces = detector.detect_faces(image)
        landmarks = detector.detect_landmarks(image, faces)
        emotions = detector.detect_emotions(image, faces, landmarks)
        au = detector.detect_aus(image, landmarks)
        

        #AUs to CSV
        file_exists = os.path.exists(output_file)
        array_data = au[0]
        
        df = pd.DataFrame(array_data, columns=au_columns)
        df.insert(0, 'image_name', file_name)  # Insert image_name in the first column
        df.insert(1, 'face_number', df.index + 1) # Insert face_number, starting from 1
        df.to_csv(output_file, index=False, header=not file_exists, mode='a')

        #Visualizing bounding boxes along with emotion
        faces = faces[0]
        landmarks = landmarks[0]
        emotions = emotions[0]
        print(f"Number of faces detected: {len(faces)}")
        print(f"Number of faces detected: {len(landmarks)}")
        print(f"Number of faces detected: {len(emotions)}")

        
        strongest_emotion = emotions.argmax(axis=1)
        for (face, top_emo) in zip(faces, strongest_emotion):
            (x0, y0, x1, y1, p) = face
            cv2.rectangle(image, (int(x0), int(y0)), (int(x1), int(y1)), (255, 0, 0), 3)
            cv2.putText(image, FEAT_EMOTION_COLUMNS[top_emo], (int(x0), int(y0 - 10)), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)
        output_path = os.path.join("freepik_dataset/dataset/images_out", file_name)
        cv2.imwrite(output_path, image)