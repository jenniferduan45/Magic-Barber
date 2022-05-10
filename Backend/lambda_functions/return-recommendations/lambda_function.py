import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    """
    main handler of events
    """
    results = []

    s3 = boto3.client('s3')
    bucket = 'ccbd-hair-dye-photos'
    recommendation_images = s3.list_objects(Bucket=bucket)['Contents']
    print(recommendation_images)

    for img in recommendation_images:
        img_url = "https://ccbd-hair-dye-photos.s3.amazonaws.com/" + img['Key']
        results.append(img_url)

    print(results)

    return {
        'statusCode': 200,
        'body': json.dumps({'results': results}),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }
