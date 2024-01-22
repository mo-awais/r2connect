from unittest import TestCase
from unittest.mock import patch

from dotenv import load_dotenv

from r2connect.r2client import R2Client
from r2connect.exceptions.cloudflare.r2 import ObjectAlreadyExists, ObjectDoesNotExist


class Test(TestCase):
    @classmethod
    @patch('boto3.resource', return_value=None)
    def setUpClass(cls, *args, **kwargs) -> None:
        load_dotenv('../.env')
        cls.__test_client = R2Client()

    @patch('r2connect.r2client.R2Client._R2Client__bucket_exists', return_value=True)
    @patch('r2connect.r2client.R2Client._R2Client__get_bucket', return_value=None)
    @patch('r2connect.r2client.R2Client._R2Client__object_exists', return_value=True)
    def test_file_upload_object_exists_exception(self, *args, **kwargs):
        with self.assertRaises(ObjectAlreadyExists):
            self.__test_client.upload_file('test', 'test', 'test')

    @patch('r2connect.r2client.R2Client._R2Client__bucket_exists', return_value=True)
    @patch('r2connect.r2client.R2Client._R2Client__object_exists', return_value=False)
    def test_file_download_object_does_not_exist_exception(self, *args, **kwargs):
        with self.assertRaises(ObjectDoesNotExist):
            self.__test_client.download_file('test', 'test', 'test')
