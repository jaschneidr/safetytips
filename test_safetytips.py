import safetytips
import unittest
import json
import datetime


class TestSafetyTips(unittest.TestCase):

    def setUp(self):
        safetytips.app.config['TESTING'] = True
        self.app = safetytips.app.test_client()

    def test_get_tips(self):
        response = self.app.get('/safetytips/api/v1.0/tips/')
        self.assertEqual(response.status_code, 200, msg="GET sent to /safetytips/api/v1.0/tips/ did not return status 200.")

    def test_create_tip(self):
        header = {'content-type': 'application/json'}
        data = json.dumps({
            'message': u'This is a test safety tip!',
            'username': u'test_tip_submitter',
        })
        response = self.app.post('/safetytips/api/v1.0/tips/', data=data, headers=header)
        self.assertEqual(response.status_code, 201, msg="response.status_code does not equal 201 and it should.")

    def test_get_tip(self):
        response = self.app.get('/safetytips/api/v1.0/tips/1')
        self.assertEqual(response.status_code, 200, msg="response.status_code does not equal 200 and it should.")

    def test_update_tip(self):
        header = {'content-type': 'application/json'}
        data = json.dumps({
            'message': u'Message has been updated!!',
            'username': u'test_tip_submitter',
        })
        response = self.app.put('/safetytips/api/v1.0/tips/1', data=data, headers=header)
        self.assertEqual(response.status_code, 201, msg="response.status_code does not equal 201 and it should.")

if __name__ == '__main__':
    unittest.main()