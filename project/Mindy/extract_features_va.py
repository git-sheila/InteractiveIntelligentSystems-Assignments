import logging #warning er niche kichu dekhabena
import math 
import os 
import pandas as pd
import numpy as np
from feat import Detector
from sklearn.ensemble import RandomForestRegressor
import joblib  # For saving models

# Initialize logging
logging.getLogger().setLevel(logging.WARNING) #warning er niche kichu dekhabena

# Initialize py-feat detector
detector = Detector() 

# Extract Action Units (AUs) from an image
def extract_aus(image_path): 
    try:
        features = detector.detect_image(image_path) 
        return features.aus.values.flatten() #2d to 1d 
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

# Load dataset
csv_path = "DiffusionFER/DiffusionEmotion_S/dataset_sheet.csv"
df = pd.read_csv(csv_path)

# Define image folder and initialize lists
image_folder = "DiffusionFER/DiffusionEmotion_S/cropped"
features, valences, arousals, labels = [], [], [], []

# Extract AUs and collect valence/arousal values
for _, row in df.iterrows(): 
    path = row['subDirectory_filePath']
    path = os.path.join(*path.split(os.sep)[1:])
    image_path = os.path.join(image_folder, path)
    
    if os.path.exists(image_path):
        feature_vector = extract_aus(image_path)
        if feature_vector is not None and not any(math.isnan(val) for val in feature_vector):
            features.append(feature_vector)
            valences.append(row['valence'])
            arousals.append(row['arousal'])
            labels.append(row['expression'])

# Convert lists to NumPy arrays
features = np.array(features)
valences = np.array(valences)
arousals = np.array(arousals)
labels = np.array(labels)

# Train models to predict valence and arousal
valence_model = RandomForestRegressor(random_state=42)
arousal_model = RandomForestRegressor(random_state=42)

valence_model.fit(features, valences)
arousal_model.fit(features, arousals)

# Save valence and arousal models
joblib.dump(valence_model, "valence_model.pkl")
joblib.dump(arousal_model, "arousal_model.pkl")
print("Valence and Arousal models saved.")

# Predict valence and arousal for all images
predicted_valences = valence_model.predict(features)
predicted_arousals = arousal_model.predict(features)

predicted_valences = [round(valence, 1) for valence in predicted_valences]
predicted_arousals = [round(arousal, 1) for arousal in predicted_arousals]

# Combine features with predicted valence and arousal
augmented_features = np.column_stack((features, predicted_valences, predicted_arousals))

# Save the augmented dataset
df_augmented = pd.DataFrame(augmented_features)
df_augmented["emotion"] = labels
df_augmented.to_csv("augmented_dataset.csv", index=False)
print("Augmented dataset saved to augmented_dataset.csv.")
