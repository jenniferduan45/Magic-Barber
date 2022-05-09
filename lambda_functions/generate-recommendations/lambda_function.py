import json
import urllib.parse
import boto3
import logging
import numpy as np
from PIL import Image
from io import BytesIO
import random

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    """
    main handler of events
    """
    # get the object from the event
    s3 = boto3.client('s3')

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    # Generate the URL to get key from bucket
    img_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': key
        }
    )
    print(img_url)

    # get input image
    response = s3.get_object(Bucket=bucket, Key=key)
    print(response)

    image = response['Body'].read()
    input_img = np.array(Image.open(BytesIO(image)))  # numpy
    print(input_img.shape)

    # uses the prediction endpoint to predict segmentation mask of the input image
    ENDPOINT_NAME = 'pytorch-inference-2022-05-07-19-52-13-234'
    sagemaker = boto3.client('sagemaker-runtime')
    content_type = "application/json"
    payload = json.dumps({'inputs': img_url})

    response = sagemaker.invoke_endpoint(EndpointName=ENDPOINT_NAME, ContentType=content_type, Body=payload)
    mask = np.array(json.loads(response['Body'].read()))

    # RGB colors for hair dye
    colors = [(255, 80, 80),  #red
              (17, 100, 47),  #green
              (50, 100, 200),  #cyan
              (255, 255, 90),  #yellow
              (254, 92, 170),  #pink
              (180, 205, 255),  #light blue
              (220, 149, 220),  #light pink
              (80, 180, 255),  #blue
              (128, 49, 167),  #grape
             ]

    n_recommendations = 3
    output_img = []
    random_colors = random.sample(colors, n_recommendations)

    input_img = input_img.astype(np.float64)
    input_img[mask] *= 0.5

    for color in random_colors:
        # Generate output hair dyed images
        print("color: ", color)
        color_mask = np.zeros_like(input_img)
        for c in range(3):
            color_mask[:, :, c] = color[c] * mask
        output_array = input_img + color_mask * 0.5
        output_img.append(output_array)

    # store to the output S3
    output_bucket = 'ccbd-hair-dye-photos'
    for i in range(n_recommendations):
        output_key = 'hair_dyed_color_{}.png'.format(i)
        output = Image.fromarray(output_img[i].astype(np.uint8))
        out_img = BytesIO()
        output.save(out_img, format='png')
        out_img.seek(0)
        response = s3.put_object(Bucket=output_bucket, Key=output_key, Body=out_img, ContentType='image/png')
        print(response)

    return {
        'statusCode': 200,
        'body': json.dumps('Finished generating recommendations')
    }
