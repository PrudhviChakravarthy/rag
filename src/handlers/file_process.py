import os
from pathlib import Path


class FileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def get_fileinfo(self) -> tuple:
        if not os.path.exists(self.file_path):
            raise ValueError("File path not found")
        file_name, file_extension = os.path.splitext(os.path.basename(self.file_path))
        print(file_name, file_extension)
        return file_name, file_extension
            
            


# 