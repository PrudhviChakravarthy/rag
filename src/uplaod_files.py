import os

def save_file_to_db(file):
    file_name = file.split("\\")[-1]
    if os.path.exists("files/"+file_name):
        return "File already uploaded plase choose another file."
    with open(file, 'rb') as f:
        with open("files/"+file_name,'wb') as w:
            w.write(f.read())

    return f"File '{file_name}' saved successfully'!"

# Retrieve all file names from the database with their IDs
