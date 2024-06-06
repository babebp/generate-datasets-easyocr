from PIL import Image, ImageDraw, ImageFont
import csv
import io
import zipfile
import os

def text_to_image(text, font_path, font_size=20):
    # Create a font object
    font = ImageFont.truetype(font_path, font_size)
    
    # Determine the size of the text to create an appropriately sized image
    dummy_img = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Create a new image with a white background
    img = Image.new('RGB', (text_width + 20, text_height + 25), "white")
    draw = ImageDraw.Draw(img)
    
    # Draw the text onto the image
    draw.text((10, 10), text, fill="black", font=font)
    
    return img

def text_file_to_images(file_path, font_path=None, font_size=20, extension='png', zip_file='output.zip', csv_file='labels.csv', text_file='labels.txt'):
    images = []
    csv_data = []
    txt_data = []

    with open(file_path, 'r', encoding='utf8') as file:
        for line_number, line in enumerate(file):
            text = line.strip()
            if text:
                image_name = f"output_line_{line_number + 1}.{extension}"
                img = text_to_image(text, font_path, font_size)
                
                # Store the image in memory
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format=extension)
                images.append((image_name, img_byte_arr.getvalue()))
                
                # Collect CSV and text data
                csv_data.append([image_name, text])
                txt_data.append(f"{image_name}\t{text}\n")
                print(f"Prepared image for line {line_number + 1} as {image_name}")

    # Create the zip file and add images and other files
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        # Write images to zip
        for image_name, image_data in images:
            zipf.writestr(image_name, image_data)
        
        # Write CSV data to zip
        csv_buffer = io.StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(['filename', 'words'])  # Write the header
        csv_writer.writerows(csv_data)
        zipf.writestr(csv_file, csv_buffer.getvalue())
        
        # Write text data to zip
        # zipf.writestr(text_file, ''.join(txt_data))
    
    print(f"All data saved to {zip_file}")

text_file_to_images("test.txt", font_path="fonts/THSarabun Bold.ttf", font_size=20, extension='png')
