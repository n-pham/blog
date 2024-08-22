+++
title = 'AWS S3 API continuation token'
featured_image = 'images/aws-s3-api-limit-continuation-token.png'
date = 2024-08-22T21:15:00+07:00
draft = false
tags = ['aws', 's3', 'limit', 'continuation', 'python']
+++
# AWS S3 ListObjects 1000 *per request*

There is a common misunderstanding that AWS S3 ListObjects returns only 1000 results.
```python
resp = s3.list_objects_v2(Bucket='gdc-mmrf-commpass-phs000748-2-open')
assert len(resp['Contents']) == 1000
```

This API and the documentation does not emphasize enough that 1000 results are *per page/request*.

We are expected to call the API multiple times while checking for `NextContinuationToken` and pass it to the next call.
```python
continuation_token = None
while True:
    api_kwargs = (
        {'ContinuationToken': continuation_token} if continuation_token
        else {}
    )
    resp = s3.list_objects_v2(
        Bucket='gdc-mmrf-commpass-phs000748-2-open',
        **api_kwargs,
    )
    print(resp['Contents'][-1]['Key'])
    continuation_token = resp.get('NextContinuationToken')
    if not continuation_token:
        break
```

This continuation/next token also applies to other AWS APIs such as Athena.


# Sample Code
```python
# %%
import boto3
from botocore import UNSIGNED
from botocore.client import Config

s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

# %%
resp = s3.list_objects_v2(Bucket='gdc-mmrf-commpass-phs000748-2-open')
print(len(resp['Contents']))  # 1000

# %%
print(resp['NextContinuationToken'])

# %%
continuation_token = None
while True:
    api_kwargs = (
        {'ContinuationToken': continuation_token} if continuation_token
        else {}
    )
    resp = s3.list_objects_v2(
        Bucket='gdc-mmrf-commpass-phs000748-2-open',
        **api_kwargs,
    )
    print(resp['Contents'][-1]['Key'])
    continuation_token = resp.get('NextContinuationToken')
    if not continuation_token:
        break
```