"""
This file contains the DataExporter class, which is responsible for 
exporting the data to a JSON file.
"""

import json

class DataExporter:
    def __init__(self, filename):
        self.filename = filename

    def export_data(self, data):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return True
        except (IOError, OSError, json.JSONDecodeError) as e:
            print(f"Error exporting data: {e}")
            return False
