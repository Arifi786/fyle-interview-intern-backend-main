import unittest
from core.libs.exceptions import FyleError  # Adjust the import path as necessary

class TestFyleError(unittest.TestCase):

    def test_initialization(self):
        # Test initialization with both status_code and message
        error = FyleError(status_code=404, message="Not Found")
        self.assertEqual(error.status_code, 404)
        self.assertEqual(error.message, "Not Found")

    def test_to_dict(self):
        # Test to_dict method
        print("here")
        error = FyleError(status_code=500, message="Internal Server Error")
        self.assertEqual(error.to_dict(), {"message": "Internal Server Error"})

    # def test_str(self):
    #     # Test string representation
    #     error = FyleError(status_code=400, message="Bad Request")
    #     self.assertEqual(str(error), "Bad Request")
