"""
This is a test file
"""

import json

data = {"name": "John Doe", "age": 30, "city": "New York"}

GLOBAL_VAR = 0

# Convert Python dictionary to JSON string
json_string = json.dumps(data, indent=4)
print(json_string)

# Convert JSON string to Python dictionary
data_loaded = json.loads(json_string)
print(
    data_loaded["name"]
    + data_loaded["name"]
    + data_loaded["name"]
    + data_loaded["name"]
)

def myunction():
    myVar = 1
    print(f"Hello World - {myVar}")
