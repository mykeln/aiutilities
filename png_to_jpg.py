import os
import sys
from PIL import Image

def convert_png_to_jpg(input_folder, output_folder, quality=85):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):
            png_image = Image.open(os.path.join(input_folder, filename))
            rgb_image = png_image.convert('RGB')
            jpg_filename = os.path.splitext(filename)[0] + '.jpg'
            rgb_image.save(os.path.join(output_folder, jpg_filename), 'JPEG', quality=quality)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python png_to_jpg_converter.py <input_folder> <output_folder> [quality]')
    else:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
        quality = int(sys.argv[3]) if len(sys.argv) > 3 else 95
        convert_png_to_jpg(input_folder, output_folder, quality)

