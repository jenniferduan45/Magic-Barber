import json
import boto3
import logging
import random
from opensearchpy import OpenSearch, RequestsHttpConnection

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def search_hair_salons(zipcode):
    """
    get a hair salons list from DynamoDB by zipcode,
    and format each hair salon as:
    {
        "BusinessId": "123456789",
        "BusinessName": "155 Barber Shop",
        "Address": "155 Manhattan Ave, New York, NY 10025",
        "PhoneNumber": "(646) 422-7200",
        "Image": "https://diana-cdn.naturallycurly.com/Articles/BP_NY-Salons-.jpg"
    }
    """
    # search hair salons by the zipcode
    auth = ('master', '6998Cloud!')
    host = 'search-yelp-data-vvi2zbhvf6zva47xatvl52w5v4.us-east-1.es.amazonaws.com'

    client = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    query = {
        'size': 1000,
        "query": {
            "range": {
                "Zip_Code": {
                    "gte": max(10000, int(zipcode) - 20),
                    "lte": min(11697, int(zipcode) + 20)
                }
            }
        }
    }

    response = client.search(
        body=query,
        index='yelp-data'
    )
    print(response)

    hair_salons_list = response['hits']['hits']
    hair_salons_list = sorted(hair_salons_list, key=lambda x: abs(int(x['_source']['Zip_Code']) - int(zipcode)))
    print("hair_salons_list size: ", len(hair_salons_list))
    print(hair_salons_list)

    if not hair_salons_list:
        return []

    # connect to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('yelp')

    results = []
    for i in range(len(hair_salons_list)):
        id = hair_salons_list[i]['_source']['business_id']
        info = table.get_item(Key={'business_id': id})['Item']

        hair_salon = {
            "BusinessId": info['business_id'],
            "BusinessName": info['name'],
            "Address": info['Address'],
            "PhoneNumber": info['phone'],
            "Rating": str(info['rating']),
            "Image": info['image_url']
        }

        results.append(hair_salon)

    return results


def lambda_handler(event, context):
    """
    main handler of events
    """
    # get the search query q from user
    zipcode = event['queryStringParameters']['q']
    print("zipcode: ", zipcode)

    results = search_hair_salons(zipcode)
    print(results)

    return {
        'statusCode': 200,
        'body': json.dumps({'results': results}),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }

