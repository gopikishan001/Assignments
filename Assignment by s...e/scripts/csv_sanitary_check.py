import csv
from io import StringIO

def csv_sanitary_check(csv_contents: str):

    expected_columns = ['S. No.', 'Product Name', 'Input Image Urls']
    error_messages = []

    csv_file = StringIO(csv_contents)
    csv_reader = csv.reader(csv_file)

    headers = next(csv_reader)
    expected_columns_error = False
    for field in expected_columns : 
        if field not in headers :
            expected_columns_error = True

    if expected_columns_error:
        error_messages.append(f"Expected columns: {expected_columns}, but found: {headers}")

    image_count = 0
    for line_num, row in enumerate(csv_reader, start=2):  
        if len(row) != len(expected_columns):
            error_messages.append(f"Row {line_num} has an incorrect number of columns.")
        else:
            urls = row[2]
            if not urls:
                error_messages.append(f"Row {line_num} has no URLs.")
            else:
                url_list = urls.split(',')
                for url in url_list:
                    if not url.startswith('http'):
                        error_messages.append(f"Row {line_num} has an invalid URL: {url}")
                    else : image_count += 1

    return error_messages, image_count
