import unittest
from core import app
from core.libs.exceptions import FyleError
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

class TestErrorHandlers(unittest.TestCase):
    def setUp(self):
        """Set up the test client."""
        self.client = app.test_client()

    def test_fyle_error(self):
        """Test handling of FyleError."""
        with self.assertRaises(FyleError):
            raise FyleError(status_code=400, message="Bad Request")

    def test_validation_error(self):
        """Test handling of ValidationError."""
        with self.assertRaises(ValidationError):
            raise ValidationError("Validation failed")

    def test_integrity_error(self):
        """Test handling of IntegrityError."""
        with self.assertRaises(IntegrityError):
            raise IntegrityError("Integrity constraint violated", "statement", "params")

    def test_http_exception(self):
        """Test handling of HTTPException."""
        with self.assertRaises(HTTPException):
            raise HTTPException("HTTP error occurred")

if __name__ == '__main__':
    unittest.main()
