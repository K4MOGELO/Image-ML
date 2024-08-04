import os

def convert_jpg_to_jpg(directory):
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        # Check if the file ends with .JPG (case-sensitive)
        if filename.endswith('.JPG'):
            # Create the new filename with .jpg extension
            new_filename = filename[:-4] + '.jpg'
            # Get the full path for renaming
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            # Rename the file
            os.rename(old_file, new_file)
            print(f'Renamed: {filename} to {new_filename}')

# Example usage
directory_path = './uploads'
convert_jpg_to_jpg(directory_path)