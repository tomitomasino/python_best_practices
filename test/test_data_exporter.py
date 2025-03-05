'''
This file contains the unit tests for the DataExporter class.
'''
import unittest
import os
import json
from export.exporter import DataExporter


class TestDataExporter(unittest.TestCase):
    def setUp(self):
        self.filename = "test_data.json"
        self.exporter = DataExporter(self.filename)
        self.test_data = {"name": "Test User", "age": 99, "city": "Test City"}

    def tearDown(self):
        # Remove the test file after each test
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_export_data_success(self):
        result = self.exporter.export_data(self.test_data)
        self.assertTrue(result)

        # Verify that the file was created and contains the correct data
        with open(self.filename, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data, self.test_data)

    def test_export_data_failure(self):
        # Mock an invalid filename to simulate a failure
        self.exporter.filename = "/invalid/path/to/file.json"
        result = self.exporter.export_data(self.test_data)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
