import os
from google.cloud import vision
from google.cloud.vision_v1 import types



# Set up Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/path/to/gcpcreds.json'

# Initialize Google Cloud client
client = vision.ImageAnnotatorClient()

# Set the directory path containing the images
dir_path = r'/path/to/images'

# Iterate through the directory and process each image
for filename in os.listdir(dir_path):
    if filename.endswith('.tiff') or filename.endswith('.png'):
        file_path = os.path.join(dir_path, filename)
        with open(file_path, 'rb') as image_file:
            content = image_file.read()

        # Perform OCR on the image
        image = types.Image(content=content)
        response = client.document_text_detection(image=image)
        text = response.full_text_annotation.text

        # Save the text to a file with the same name as the image
        output_path = os.path.join(dir_path, os.path.splitext(filename)[0] + '.txt')
        with open(output_path, 'w') as output_file:
            output_file.write(filename + '\n')  # Write the filename as the first line
            output_file.write(text)

        print(f'Processed {filename} and saved the text to {output_path}.')

# Merge all the text files into a single file
output_file_path = os.path.join(dir_path, 'output.txt')
with open(output_file_path, 'w') as output_file:
    for filename in os.listdir(dir_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(dir_path, filename)
            with open(file_path, 'r') as input_file:
                output_file.write(input_file.read())

print(f'Merged all the text files into {output_file_path}.')
