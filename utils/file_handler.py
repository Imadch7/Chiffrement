import os
import json

def load_json_file(path):
    """
    Validates, opens, and parses a JSON file.
    
    Args:
        path (str): The relative or absolute path to the file.
        
    Returns:
        dict: The parsed JSON data, or an empty dict if an error occurs.
    """

    if not os.path.exists(path):
        raise ValueError(f"File path {path} does not exist")

    _, file_ext = os.path.splitext(path)
    if not file_ext or file_ext.lower() != ".json":
        raise ValueError(f"File {path}, is not a JSON file ❌")
    
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
        
    except FileNotFoundError:
        print(f"File {path} not found ❌")
        return {}
    
    except json.JSONDecodeError as e:
        print(f"File {path} contains invalid JSON format:{e} ❌")
        return {}
    
    except PermissionError:
        print(f"Permission to read {path} denied")
        return {}
    
def save_to_json_file(path, data):
    """
    Saves data specifically in JSON format within the ./usr_data directory.
    """

    if not path:
        raise ValueError(f"A file path must be passed, {path} not accepted")
    
    if data is None:
        raise ValueError(f"Data must be passed.")
    
    if not os.path.exists("./output"):
        os.makedirs("./output")
        
    try:
        with open(path, "w") as file:
            json.dump(data, file, indent=4)
        
    except PermissionError:
        print(f"Permission to write to ({path}) has been denied")
    
def save_to_file(filename, data, ext=".txt"):
    """
    Generic file saver. Redirects to JSON logic or saves as plain text.
    """

    if not filename:
        raise ValueError(f"A file path must be passed, {filename} not accepted")
    
    if not data:
        raise ValueError(f"Data must be passed")
    
    if ext.lower() == ".json":
        return save_to_json_file(filename, data)
    
    # Ensure the storage directory exists
    if not os.path.exists("./usr_data"):
        os.makedirs("./usr_data")
            
    # Ensure the filename ends with the correct extension
    if not filename.endswith(ext):
        full_path = os.path.join("./user_data", filename, ext)
    else:
        full_path = os.path.join("./user_data", filename)
    
    try:
        with open(full_path, "w", encoding="utf-8") as file:
            file.write(str(data))
    
    except PermissionError:
        print(f"Permission to write to {full_path} has been denied")