import os, json

def file_exists(file_path):
    return os.path.isfile(file_path)

def read_json(file_path):
    with open(file_path) as f:
        return json.load(f)
    
def read_file(file_path):
    with open(file_path, "r") as f:
        return f.readlines()
    
def write_file(file_path, file_content):
    with open(file_path, 'w') as w:
        for line in file_content:
            w.write(line)
    
