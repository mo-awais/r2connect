# R2 Gateway

The R2Gateway Python module provides a convenient interface for performing common operations on AWS S3 buckets while being compatible with Cloudflare's R2 service. It allows you to create, delete, upload, download and delete objects in an S3 bucket. It also allows creating and deleting buckets, handling various exceptions that might occur during these operations.

## Table of Contents

 - Installation
 - Initialisation
 - Usage
	 - Create a Bucket
	 - Delete a Bucket
	 - Upload a File
	 - Download a File
	 - Delete a File
 - Exception Handling

## Installation

You can install the **r2gateway** module using pip:

```bash
pip install r2gateway
```

## Initialisation

Before initialising an **R2Client** class, make sure to set the following environment variables:

 - **ENDPOINT_URL**: The endpoint URL for your AWS S3 or Cloudflare R2 service.
 - **ACCESS_KEY**: Your AWS S3 or Cloudflare R2 access key.
 - **SECRET_KEY**: Your AWS S3 or Cloudflare R2 secret key.
 - **REGION**: The AWS S3 region (*Cloudflare doesn't require a region but defaults to **us-east-1***)

To initialise an R2Client class, follow the example below:

```python
from r2gateway.utils.cloudflare.r2client import R2Client

try:
	r2_client = R2Client()
except r2gateway.exceptions.cloudflare.r2.MissingConfig as error:
	# A required environment variable is missing
	print(error)
```

## Usage

To use the **R2Client** class, follow the examples below:

### Create a Bucket

```python
from r2gateway.utils.cloudflare.r2client import R2Client

# Initialise the R2Client class (as shown in the previous section)
# ...

bucket_name = "my-new-bucket"

try:
    r2_client.create_bucket(bucket_name)
except r2gateway.exceptions.cloudflare.r2.BucketAlreadyExists as error:
    print(f"The specified bucket already exists: {bucket_name}")
except Exception as error:
    print(error)
```

### Delete a Bucket

A bucket can be deleted in two ways. If the bucket is not empty you can attempt a safe delete which will only delete if the bucket is empty.
You can also set the `force_delete` flag to True which will delete the bucket and its contents. Below is an example for each:

##### Safe delete a bucket

```python
from r2gateway.utils.cloudflare.r2client import R2Client

# Initialise the R2Client class (as shown in the previous section)
# ...

bucket_name = "my-existing-bucket"

try:
    r2_client.delete(bucket_name)
except r2gateway.exceptions.cloudflare.r2.BucketDoesNotExist as error:
    print(f"The specified bucket does not exist: {bucket_name}")
except r2gateway.exceptions.cloudflare.r2.BucketIsNotEmpty as error:
    print(f"The specified bucket is not empty, cannt safe delete: {bucket_name}")
except Exception as error:
    print(error)
```

##### Force delete a bucket

```python
from r2gateway.utils.cloudflare.r2client import R2Client

# Initialise the R2Client class (as shown in the previous section)
# ...

bucket_name = "my-existing-bucket"

try:
    r2_client.delete(bucket_name, force_delete=True)
except r2gateway.exceptions.cloudflare.r2.BucketDoesNotExist as error:
    print(f"The specified bucket does not exist: {bucket_name}")
except Exception as error:
    print(error)
```

### Upload a File

```python
from r2gateway.utils.cloudflare.r2client import R2Client

# Initialise the R2Client class (as shown in the previous section)
# ...

bucket_name = "my-existing-bucket"
file_path = "path/to/you/file.txt"
object_name = "file.txt"

try:
	r2_client.upload_file(file_path, object_name, bucket_name)
except r2gateway.exceptions.cloudflare.r2.BucketDoesNotExist as error:
	print(f"The specified bucket does not exist: {bucket_name}")
except r2gateway.exceptions.cloudflare.r2.ObjectAlreadyExists as error:
	print(f"An object with the same object_key already exists: {object_name}")
except Exception as error:
	print(error)
```

### Download a File

A save filepath can be specified but is not required. If one isn't provided, the file will be saved in the same execution level
with the **user_id** as the prefix and the **filename** as the suffix.

```python
from r2gateway.utils.cloudflare.r2client import R2Client

# Initialise the R2Client class (as shown in the previous section)
# ...

bucket_name = "my-existing-bucket"
download_file_path = "path/to/you/file.txt"
object_name = "file.txt"

try:
	r2_client.download_file(object_name, bucket_name, download_file_path)
except r2gateway.exceptions.cloudflare.r2.ObjectDoesNotExist as error:
	print(f"The specified file does not exist: {object_name}")
except r2gateway.exceptions.cloudflare.r2.BucketDoesNotExist as error:
	print(f"The specified bucket does not exist: {bucket_name}")
except Exception as error:
	print(error)
```

### Delete a File

```python
from r2gateway.utils.cloudflare.r2client import R2Client

# Initialise the R2Client class (as shown in the previous section)
# ...

bucket_name = "my-existing-bucket"
object_name = "file.txt"

try:
	r2_client.delete_file(object_name, bucket_name)
except r2gateway.exceptions.cloudflare.r2.ObjectDoesNotExist as error:
	print(f"The specified object does not exist in this bucket: {object_name}")
except r2gateway.exceptions.cloudflare.r2.BucketDoesNotExist as error:
	print(f"The specified bucket does not exist: {bucket_name}")
except Exception as error:
	print(error)
```

## Exception Handling

The **R2Gateway** module provides exception handling for various scenarios.

- **BucketAlreadyExists**: Raised when attempting to create a bucket that already exists.
- **BucketDoesNotExist**: Raised when the specified bucket does not exist.
- **BucketIsNotEmpty**: Raised when trying to delete a non-empty bucket without specifying `force_delete=True`
- **ObjectDoesNotExist**: Raised when attempting operation on a non-existing object.
- **ObjectAlreadyExists**: Raised when trying to upload an object with the same name as an existing object.
- **MissingConfig**: Raised when trying to initialise an `R2Client` object without the required environment variables.