import json
import csv
import time
from collections import defaultdict
import simplejson as json
import boto3
from datetime import datetime
import requests
from decimal import *
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection
import uuid

session = boto3.Session()

def lambda_handler (event, context):    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('yelp')
    API_KEY = 'ECFNcAjrYLgEQUhZZAj9BFpRPBNwJVFu6RQcchve8o6hqQmmyuLm4Jj0uNP47A3kMfV9MIXtG8qkOlPXckub3PJxmW378dEvfvPUIbsg_ddDqnzDuu0lPUKnHocVYnYx' 
    ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
    ENDPOINT_ID = 'https://api.yelp.com/v3/businesses/' # + {id}
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}
    PARAMETERS = {'term': 'hair', 
              'limit': 50,
              'radius': 10000,
              'offset': 200,
              'location': 'Manhattan'}


    manhattan_nbhds = ['Lower East Side, Manhattan',
                    'Upper East Side, Manhattan',
                    'Upper West Side, Manhattan',
                    'Washington Heights, Manhattan',
                    'Central Harlem, Manhattan',
                    'Chelsea, Manhattan',
                    'Manhattan',
                    'East Harlem, Manhattan',
                    'Gramercy Park, Manhattan',
                    'Greenwich, Manhattan',
                    'Lower Manhattan, Manhattan']

    index_id = 0
    for nbhd in manhattan_nbhds:
        PARAMETERS['location'] = nbhd
        response = requests.get(url = ENDPOINT, params =  PARAMETERS, headers=HEADERS).json()
        print(response)
        business_data = response['businesses']
        for business in business_data:
            table.put_item(
                Item = {
                        'business_id':is_null(business['id']),
                        'name':  is_null(business['name']),
                        'rating': is_null(Decimal(business['rating'])),
                        'Number_of_Reviews' : is_null(Decimal(business['review_count'])),
                        'Address': is_null(business['location']['address1']) + ', ' + is_null(business['location']['city']) + ', ' + is_null(business['location']['state']) + ', ' + is_null(business['location']['zip_code']),
                        'Zip_Code': is_null(business['location']['zip_code']),
                        'Latitude': is_null(str(business['coordinates']['latitude'])),
                        'Longitude': is_null(str(business['coordinates']['longitude'])),
                        'image_url': is_null(str(business['image_url'])),
                        'phone': is_null(str(business['phone']))
                    }
            )

            json_object = {
                'business_id': is_null(business['id']),
                'Zip_Code': is_null(business['location']['zip_code'])
            }
            print(json_object)
            store_es('yelp-data', json_object, uuid.uuid4())
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }

def is_null (input):
    if len(str(input)) == 0:
        return 'N/A'
    else:
        return input
        
def store_es(index_name, document, id):
    region = 'us-east-1'
    service = 'es'
    credentials = session.get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    endpoint = 'search-yelp-data-vvi2zbhvf6zva47xatvl52w5v4.us-east-1.es.amazonaws.com'
    client = OpenSearch(
            hosts=[{'host': endpoint, 'port': 443}],
            use_ssl=True,
            verify_certs=True,
            http_auth=awsauth,
            connection_class=RequestsHttpConnection)
    response = client.index(
            index = index_name,
            body = document,
            id = id,
            refresh = True)
    print(response) 
    
