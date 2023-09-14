import os
import uuid

import boto3

from utils.files.filepath import Filepath
from exceptions.cloudflare.r2 import *


class R2:
    def __init__(self) -> None:
        """
        Initialise the S3 client that will be used with the Cloudflare R2 services.
        """

        self.__r2_resource = boto3.resource(
            "s3",
            endpoint_url=os.environ.get("ENDPOINT_URL"),
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_KEY"),
            region_name=os.environ.get("REGION")
        )

        self.__location_constraint = {"LocationConstraint": os.environ.get("REGION")}

    def __bucket_exists(self, bucket_name: str) -> bool:
        """
        Check if the specified bucket exits

        :param bucket_name: The bucket name to check
        :type: str
        :returns: bool
        """

        for bucket in self.__r2_resource.buckets.all():
            if bucket.name == bucket_name:
                return True

        return False

    def __object_exists(self, bucket_name: str, object_name: str) -> bool:
        """
        Check if the specified object exists in the specified bucket

        :param bucket_name: The bucket to check
        :param object_name: The object to search for
        :returns: bool
        """

        bucket = self.__get_bucket(bucket_name)

        if list(bucket.objects.filter(Prefix=object_name)):
            return True
        else:
            return False

    def __get_object(self, bucket_name: str, object_name: str):
        """
        Get specified object from specified bucket and return as boto3 Object

        :param bucket_name: The bucket to check
        :param object_name: The object to fetch
        :returns: boto3 Object
        """

        return self.__r2_resource.Object(bucket_name, object_name)

    def __get_bucket(self, bucket_name: str):
        """
        Return a bucket instance using the specified bucket name

        :param bucket_name: The bucket which is being queried
        :return: A boto3 Bucket instance
        """

        return self.__r2_resource.Bucket(bucket_name)

    def __bucket_empty(self, bucket_name: str) -> bool:
        """
        Check if the specified bucket is empty

        :param bucket_name: The bucket name to check
        :type: str
        :returns: bool
        """

        bucket = self.__get_bucket(bucket_name)

        if len(list(bucket.objects.all())) > 0:
            return False
        else:
            return True

    def __purge_bucket(self, bucket_name: str) -> None:
        """
        Delete all items in a specified bucket

        :param bucket_name: The bucket to be purged
        :type: str
        :returns: None
        """

        bucket = self.__get_bucket(bucket_name)

        for r2_object in bucket.objects.all():
            r2_object.delete()

    def create_bucket(self, bucket_name: str) -> None:
        """
        Create a new bucket with the specified name

        :param bucket_name: Bucket name for new bucket
        :type: str
        :raises BucketNotFound: If bucket already exists
        :returns: None
        """

        if self.__bucket_exists(bucket_name):
            raise BucketAlreadyExists(f"The following bucket already exists: {bucket_name}")
        else:
            self.__r2_resource.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": "us-east-1"
                }
            )

    def delete_bucket(self, bucket_name: str, force_delete: bool = False) -> None:
        """
        Delete a bucket with the specified name

        :param bucket_name: The bucket to be deleted
        :type: str
        :param force_delete: Force delete a non-empty bucket
        :type: bool
        :raises BucketIsNotEmpty: If specified bucket contains object and force_delete flag is not set
        :raises BucketDoesNotExist: If specified bucket does not exist
        :returns: None
        """

        if self.__bucket_exists(bucket_name):
            if self.__bucket_empty(bucket_name) or force_delete:
                self.__purge_bucket(bucket_name)

                bucket = self.__get_bucket(bucket_name)
                bucket.delete()
            else:
                raise BucketIsNotEmpty(f"The following bucket must be empty before deleting: {bucket_name}")
        else:
            raise BucketDoesNotExist(f"The following bucket does not exist: {bucket_name}")

    def upload_file(self, filepath: str, object_name: str, bucket_name: str) -> None:
        """
        Upload a file to a specified bucket with a specified value to save as

        :param filepath: Filepath location of the file which must be uploaded
        :param object_name: String name to save the file as
        :param bucket_name: Bucket for file to be saved in
        :type: str
        :returns: None
        :raises BucketDoesNotExist: If specified bucket does not exist
        """

        if self.__bucket_exists(bucket_name):
            bucket = self.__get_bucket(bucket_name)
            clean_filepath = Filepath.safe_filepath(filepath)
            clean_object_name = Filepath.safe_filepath(object_name)

            bucket.upload_file(
                Filename=clean_filepath,
                Key=clean_object_name
            )
        else:
            raise BucketDoesNotExist(f"The following bucket does not exist: {bucket_name}")

    def download_file(self, object_name: str, save_path: str, bucket_name: str) -> str:
        """
        Download a specified object from a specified bucket

        :param object_name: The object to download
        :param save_path: The location to temporarily save the object
        :param bucket_name: The bucket to download from
        :returns: Hash string of the temporary file name
        """

        temporary_filename = str(uuid.uuid4()) + "." + object_name.split(".")[1]

        r2_object = self.__get_object(bucket_name, object_name)
        r2_object.download_file(save_path + temporary_filename)

        return temporary_filename

    def delete_file(self, object_name: str, bucket_name: str) -> None:
        """
        Delete an object from a specified bucket

        :param object_name: The object which must be deleted
        :param bucket_name: The bucket to delete from
        :raises BucketDoesNotExist: If the specified bucket does not exist
        :raises ObjectDoesNotExist: If the specified object does not exist
        :returns: None
        """

        if self.__bucket_exists(bucket_name):
            if self.__object_exists(bucket_name, object_name):
                self.__get_object(bucket_name, object_name).delete()
            else:
                raise ObjectDoesNotExist(f"The following object does not exist in {bucket_name}: {object_name}")
        else:
            raise BucketDoesNotExist(f"The following bucket does not exist: {bucket_name}")
