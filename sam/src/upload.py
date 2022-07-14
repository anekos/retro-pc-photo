from io import BytesIO
from typing import Any
import base64
import json
import uuid

import boto3
from PIL import Image


s3_resource = boto3.resource('s3')


def lambda_handler(event: Any, context: Any) -> Any:
    # print('Received event: ' + json.dumps(event, indent=2))

    method = event['requestContext']['http']['method']
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': 'https://rpp.snca.net/*',


                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST'
            }
        }

    body = base64.b64decode(event['body'])
    img = Image.open(BytesIO(body))

    if 640 < img.width or 480 < img.height:
        raise Exception('Too large: {}x{}'.format(img.width, img.height))

    print({'width': img.width, 'height': img.height})

    # bucket = 'retro-pc-photo-bucketweb-1odrwqqjtomka'
    # filename = 'u/' + str(uuid.uuid4()) + '.png'
    # url =

    bucket = 'gyazo.snca.net'
    filename = 'rpp/' + str(uuid.uuid4()) + '.png'
    url = 'https://ozayg.snca.net/' + filename

    s3_resource.Bucket(bucket).put_object(
        Key=filename, Body=body, ContentType='image/png'
    )

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'url': url})
    }
