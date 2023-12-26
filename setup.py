from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "boto3==1.28.63",
    "botocore==1.31.63",
    "jmespath==1.0.1",
    "python-dateutil==2.8.2",
    "s3transfer==0.7.0",
    "six==1.16.0",
    "urllib3==2.0.7"
]

setup(
    name="r2connect",
    version="1.1.2",
    author="Mohammed Awais",
    author_email="awais@mohammedawais.me",
    description="R2Connect is a powerful Python module designed for seamless integration between AWS S3 and Cloudflare's R2 service. It offers a simple and intuitive interface to create, manage, and synchronize buckets, objects, and data, facilitating efficient backend operations in a reliable and secure manner. Streamline your S3 and R2 interactions with R2Connect.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/mo-awais/r2connect",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
)