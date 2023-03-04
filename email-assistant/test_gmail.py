import unittest
import gmail

class TestGmail(unittest.TestCase):
    def test_auth(self):
        # We want to check that the object created is not None
        obj = gmail.gmail_authenticate()
        print(type(obj))
        self.assertTrue(type(obj), 'googleapiclient.discovery.Resource')

    def test_add_attachment(self):
        pass

    def test_build_message(self):
        body = 'this is a test message'
        msg_container = gmail.build_message('test@gmail.com', 'test', body)
        self.assertTrue(type(msg_container), 'dict')

    def test_send_message(self):
        service = gmail.gmail_authenticate()
        body = 'this is a test message'
        gmail.send_message(service, 'test@test.com', 'test', body)

    def test_search_messages(self):
        service = gmail.gmail_authenticate()
        query = 'test'
        result = gmail.search_messages(service, query)
        self.assertTrue(result, '2')


if __name__ == '__main__':
    unittest.main()