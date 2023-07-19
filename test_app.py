"""
Importing necessary packages and modules.
"""
import unittest
from app import app


class AppTestCase(unittest.TestCase):
    """
    Test case class for testing the Flask app routes.

    This class contains test cases to validate the functionality of the Flask app routes.
    """

    def setUp(self):
        """
        Set up the Flask app for testing.

        This method is automatically executed before each individual test case.
        It configures the app in testing mode and creates a test client for making requests.
        """
        app.testing = True
        self.client = app.test_client()

    def test_transform_data_route(self):
        """
        Test the 'transform_data' route.

        This test case sends a GET request to the 'transform_data' route and checks if
        the response status code is 200 (OK). It also checks if the response content
        contains the expected HTML content indicating successful data transformation.
        """
        response = self.client.get('/transform')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Data transformation completed.", response.data)


if __name__ == '__main__':
    unittest.main()
