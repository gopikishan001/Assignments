# scripts/process_images.py
from PIL import Image
import os

def process_image(input_path: str, output_path: str):
    with Image.open(input_path) as img:
        width, height = img.size
        img = img.resize((width // 2, height // 2))  
        img.save(output_path)

async def process_images(images, input_dir, output_dir):

    try : 
        for id in images :
            input_path = f"{input_dir}/{id}.jpg"
            output_path = f"{output_dir}/{id}.jpg"
            if os.path.isfile(input_path):
                process_image(input_path, output_path)
        
        return True
    
    except Exception as e:
        return False
            
