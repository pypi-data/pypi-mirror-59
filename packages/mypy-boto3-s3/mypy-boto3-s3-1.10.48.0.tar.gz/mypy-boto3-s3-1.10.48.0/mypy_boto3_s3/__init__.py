"""
Main interface for s3 service.

Usage::

    import boto3
    from mypy_boto3.s3 import (
        BucketExistsWaiter,
        BucketNotExistsWaiter,
        Client,
        ListMultipartUploadsPaginator,
        ListObjectVersionsPaginator,
        ListObjectsPaginator,
        ListObjectsV2Paginator,
        ListPartsPaginator,
        ObjectExistsWaiter,
        ObjectNotExistsWaiter,
        S3Client,
        S3ServiceResource,
        ServiceResource,
        )

    session = boto3.Session()

    client: S3Client = boto3.client("s3")
    session_client: S3Client = session.client("s3")

    resource: S3ServiceResource = boto3.resource("s3")
    session_resource: S3ServiceResource = session.resource("s3")

    bucket_exists_waiter: BucketExistsWaiter = client.get_waiter("bucket_exists")
    bucket_not_exists_waiter: BucketNotExistsWaiter = client.get_waiter("bucket_not_exists")
    object_exists_waiter: ObjectExistsWaiter = client.get_waiter("object_exists")
    object_not_exists_waiter: ObjectNotExistsWaiter = client.get_waiter("object_not_exists")

    list_multipart_uploads_paginator: ListMultipartUploadsPaginator = client.get_paginator("list_multipart_uploads")
    list_object_versions_paginator: ListObjectVersionsPaginator = client.get_paginator("list_object_versions")
    list_objects_paginator: ListObjectsPaginator = client.get_paginator("list_objects")
    list_objects_v2_paginator: ListObjectsV2Paginator = client.get_paginator("list_objects_v2")
    list_parts_paginator: ListPartsPaginator = client.get_paginator("list_parts")
"""
from mypy_boto3_s3.client import S3Client as Client, S3Client
from mypy_boto3_s3.paginator import (
    ListMultipartUploadsPaginator,
    ListObjectVersionsPaginator,
    ListObjectsPaginator,
    ListObjectsV2Paginator,
    ListPartsPaginator,
)
from mypy_boto3_s3.service_resource import S3ServiceResource, S3ServiceResource as ServiceResource
from mypy_boto3_s3.waiter import (
    BucketExistsWaiter,
    BucketNotExistsWaiter,
    ObjectExistsWaiter,
    ObjectNotExistsWaiter,
)


__all__ = (
    "BucketExistsWaiter",
    "BucketNotExistsWaiter",
    "Client",
    "ListMultipartUploadsPaginator",
    "ListObjectVersionsPaginator",
    "ListObjectsPaginator",
    "ListObjectsV2Paginator",
    "ListPartsPaginator",
    "ObjectExistsWaiter",
    "ObjectNotExistsWaiter",
    "S3Client",
    "S3ServiceResource",
    "ServiceResource",
)
