import os

# Directory where your JPEG files are located
directory = 'uploads'

for filename in os.listdir(directory):
    if filename.endswith(".jpeg"):
        # Construct full file path
        old_file = os.path.join(directory, filename)
        # Replace .jpeg with .jpg
        new_file = os.path.join(directory, filename[:-5] + ".jpg")
        # Rename the file
        os.rename(old_file, new_file)


print("File extensions changed from .jpeg to .jpg")