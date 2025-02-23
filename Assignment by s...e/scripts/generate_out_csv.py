# scripts/generate_out_csv.py
import csv
import os

async def generate_out_csv(images, unique_file_name, out_dir):
    
    try :
        current_directory = os.getcwd() 

        temp = {}
        for image in images:
            info = image.split(">")           # f"{reference_number}>{sno}>{product_name}>{counter}"
            sno = info[1]
            product_name = info[2]
            link = images[image]
            offline_path_raw = os.path.join(current_directory, "/data/raw_images/", image + ".jpg" )
            offline_path_processed = os.path.join(current_directory, "/data/processed_images/", image + ".jpg")

            if sno not in temp : temp[sno] = {'product_name' : product_name , 'link' : [] , 'offline_path_raw' : [], 'offline_path_processed' : []}
            temp[sno]['link'].append(link)
            temp[sno]['offline_path_raw'].append(offline_path_raw)
            temp[sno]['offline_path_processed'].append(offline_path_processed)

        data = {"S. No." : [], "Product Name" : [], "Input Image Urls" : [], "Input Image path" : [], "Processed Image path" : []}

        for sno in temp :
            data["S. No."].append(sno)
            data["Product Name"].append(temp[sno]["product_name"])
            data["Input Image Urls"].append(",".join(temp[sno]["link"]))
            data["Input Image path"].append(",".join(temp[sno]["offline_path_raw"]))
            data["Processed Image path"].append(",".join(temp[sno]["offline_path_processed"]))

        header = data.keys()
        rows = zip(*data.values())
        with open(out_dir + "/" + unique_file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Writing the header
            writer.writerows(rows) 

        return True 
    
    except Exception as e: 
        return False