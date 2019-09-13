import unittest

from flask_example import application


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = application.test_client()

    def test_server(self):
        resp = self.client.get('/cusip/123456789')
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get('/security/123456789')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data[0]['cusip'], '123456789')

    def test_not_there(self):
        resp = self.client.get('/security/BETTERNOTBETHERE')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data['status'], 'Not found')


if __name__ == '__main__':
    unittest.main()
