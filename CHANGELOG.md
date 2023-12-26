# Changelog

All notable changes to the current version this project will be documented in
this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2023-10-20

### Changed

- Add `region` parameter to `create_bucket` method for AWS compatibility.

## [1.1.2] - 2023-12-26

### Added

- Add Unit Tests

### Changed

- Fixed incorrect exception in docstring from `BucketNotFound` to `BucketAlreadyExists`
- Upgraded urllib3 from `2.0.6` to `2.0.7` to patch information exposure vulnerability