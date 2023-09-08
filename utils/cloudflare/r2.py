import os
import json

import boto3

from exceptions.cloudflare.r2 import BucketAlreadyExists, BucketIsNotEmpty, BucketDoesNotExist


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
