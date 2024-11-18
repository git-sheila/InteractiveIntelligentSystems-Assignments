#import cv2
import os
import numpy as np
#import opencv_jupyter_ui as jcv2
#from feat import Detector
#from IPython.display import Image
#from PIL import Image as PILImage
#from feat.utils import FEAT_EMOTION_COLUMNS
import csv
import pandas as pd
import matplotlib.pyplot as plt


# Read the annotations.csv into a DataFrame csv1
csv1 = pd.read_csv('freepik_dataset\\dataset\\annotations.csv', names=['file', 'valence'])

# Read the output from part 1 into a DataFrame csv2
csv2 = pd.read_csv('output.csv', skiprows=1, names=['image_name', 'face_number', 'AU00', 'AU01', 'AU02', 'AU03', 'AU04', 'AU05', 'AU06', 'AU07', 'AU08', 'AU09', 'AU10', 'AU11', 'AU12', 'AU13', 'AU14', 'AU15', 'AU16', 'AU17', 'AU18', 'AU19'])
csv2['image_name'] = csv2['image_name'].str.replace('.jpg', '', regex=False)

# Merge csv1 and csv2 on the 'key' column
df_merged = pd.merge(csv2, csv1, left_on='image_name', right_on='file', how='left')
df_merged = df_merged.drop(columns=['file'])

# Reorder columns to move 'valence' to the second position
columns = ['image_name'] + ['valence'] + [col for col in df_merged.columns if col not in ['image_name', 'valence']]
df_merged = df_merged[columns]


au_columns = [col for col in df_merged.columns if col.startswith('AU')]  # List of AU columns
df_mean = df_merged.groupby('valence')[au_columns].mean()

# Calculate the absolute difference between the positive and negative means for each AU
#df_positive = df_merged[df_merged['valence'] == 'positive']
#df_negative = df_merged[df_merged['valence'] == 'negative']
positive_mean = df_mean.loc['positive']
negative_mean = df_mean.loc['negative']
absolute_diff = abs(positive_mean - negative_mean)

# Sort the AUs by the absolute difference from largest to smallest
sorted_diff = absolute_diff.sort_values(ascending=False)
#print(sorted_diff)

# Save the sorted differences to a new CSV if needed
sorted_diff.to_csv('sorted_absolute_differences.csv')

# Plotting the results
plt.figure(figsize=(10, 6))
plt.scatter(sorted_diff.index, sorted_diff.values, color='blue', marker='o')

# Annotate each point with the AU name
for i, value in enumerate(sorted_diff.values):
    plt.text(sorted_diff.index[i], value + 0.01, sorted_diff.index[i], ha='center', va='bottom', fontsize=9)

# Set the x-axis label and y-axis label
plt.xlabel('Action Units (AU)', fontsize=12)
plt.ylabel('Absolute Difference of Means', fontsize=12)
plt.title('Absolute Difference of Means for Each AU (Positive vs Negative)', fontsize=14)
plt.grid(True)

# Save the plot as a PNG file
plt.savefig('au_visualization.png')
plt.show()

# Save the merged DataFrame to a new CSV if needed
#df_merged.to_csv('merged_output.csv', index=False)
# Print the merged DataFrame to verify
#print(df_merged)

