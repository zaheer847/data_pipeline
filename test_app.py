import unittest
from app import app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_transform_data_route(self):
        response = self.client.get('/transform')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Data transformation completed.", response.data)

if __name__ == '__main__':
    unittest.main()
