import json

def readJsonFile(file: str) -> dict:
    try:
        with open(file, 'r') as f:
            data_dict = json.load(f)
        #print("JSON data successfully loaded into a dictionary:")
        return data_dict
    except FileNotFoundError:
        print(f"Error: The file 'your_file_name.json' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from 'your_file_name.json'. Check file format.")
        return None


