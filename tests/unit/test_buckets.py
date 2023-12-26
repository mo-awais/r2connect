from unittest import TestCase
from unittest.mock import Mock, patch

from dotenv import load_dotenv

from r2connect.r2client import R2Client
from r2connect.exceptions.cloudflare.r2 import BucketAlreadyExists, BucketDoesNotExist, BucketIsNotEmpty


class Test(TestCase):
    @classmethod
    @patch('boto3.resource', return_value=None)
    def setUpClass(cls, *args, **kwargs) -> None:
        load_dotenv('../.env')
        cls.__test_client = R2Client()

    @patch('r2connect.r2client.R2Client._R2Client__bucket_exists', return_value=False)
    def test_delete_non_existent_bucket_exception(self, *args, **kwargs):
        with self.assertRaises(BucketDoesNotExist):
            self.__test_client.delete_bucket('test_bucket')

    @patch('r2connect.r2client.R2Client._R2Client__bucket_exists', return_value=True)
    @patch('r2connect.r2client.R2Client._R2Client__bucket_empty', return_value=False)
    def test_delete_non_empty_bucket_exception(self, *args, **kwargs):
        with self.assertRaises(BucketIsNotEmpty):
            self.__test_client.delete_bucket('test_bucket')

    @patch('r2connect.r2client.R2Client._R2Client__bucket_exists', return_value=True)
    def test_create_bucket_exception(self, *args, **kwargs):
        with self.assertRaises(BucketAlreadyExists):
            self.__test_client.create_bucket('test_bucket', 'us-east-1')
