import os
import shutil
import random

class PreprocessFaces:
    def __init__(self, source_dir, target_dir, train_ratio=0.8):
        """
        Initializes the PreprocessFaces class.

        Args:
            source_dir (str): Path to the source directory containing the dataset.
            target_dir (str): Path to the target directory where the organized data will be stored.
            train_ratio (float): The ratio of training data to total data (default is 0.8).
        """
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.train_ratio = train_ratio

    def create_target_directories(self):
        """
        Creates the target directory structure for each emotion category with train and test splits.
        """
        emotions = ['anger', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']

        for emotion in emotions:
            for split in ['train', 'test']:
                dir_path = os.path.join(self.target_dir, split, emotion)
                os.makedirs(dir_path, exist_ok=True)

    def add_to_target(self):
        """
        Processes the images and organizes them into the new directory structure.
        """
        self.create_target_directories()

        # Walk through the source directory
        for subdir, _, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith('.jpg'):
                    # Extract the emotion label from the filename
                    emotion_label = file.split('.')[0]  # Assumes filenames like 'happiness.jpg'
                    subject_name = os.path.basename(subdir)  # e.g., 'man_sub1'

                    # Determine gender randomly (50/50 chance)
                    gender = random.choice(['male', 'female'])

                    # Check if the emotion label is valid
                    if emotion_label in ['anger', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']:
                        source_path = os.path.join(subdir, file)

                        # Create unique naming
                        count = len(os.listdir(os.path.join(self.target_dir, 'train', emotion_label))) + \
                                len(os.listdir(os.path.join(self.target_dir, 'test', emotion_label))) + 1
                        unique_name = f"{emotion_label}_{gender}_{count}.jpg"

                        # Split data into train and test
                        if random.random() < self.train_ratio:
                            target_path = os.path.join(self.target_dir, 'train', emotion_label, unique_name)
                        else:
                            target_path = os.path.join(self.target_dir, 'test', emotion_label, unique_name)

                        # Copy the image to the target directory
                        shutil.copy(source_path, target_path)

        print(f"Preprocessing complete. Images have been organized in: {self.target_dir}")

# Example usage:
if __name__ == "__main__":
    source_directory = 'dataset/imported_faces'  # Correct path for your dataset
    target_directory = 'dataset/faces_dataset'  # Desired output directory

    preprocessor = PreprocessFaces(source_directory, target_directory)
    preprocessor.add_to_target()
