# You need use this example code in to the main folder
from __future__ import print_function
import time
import meli
from meli.rest import ApiException
from pprint import pprint
import csv

def get_cats():
    # Defining the host, defaults to https://api.mercadolibre.com
    # See configuration.py for a list of all supported configuration parameters.
    configuration = meli.Configuration(
        host = "https://api.mercadolibre.com"
    )

    #https://auth.mercadolibre.com.co/authorization?response_type=code&client_id=5052533537567494&redirect_uri=https://127.0.0.1:5000


    # Enter a context with an instance of the API client
    with meli.ApiClient() as api_client:
    # Create an instance of the API class
        api_instance = meli.OAuth20Api(api_client)
        grant_type = 'authorization_code' # or 'refresh_token' if you need get one new token
        client_id = '5052533537567494' # Your client_id
        client_secret = 'N6opXnSFgJRcqNLwUY4kI3rzM8Fuxz4q' # Your client_secret
        redirect_uri = 'https://127.0.0.1:5000' # Your redirect_uri
        code = 'TG-62f8198865e7e40001dd82d4-1167652302' # The parameter CODE, empty if your send a refresh_token
        refresh_token = '' # Your refresh_token

        api_instance = meli.RestClientApi(api_client)
        resource = '/sites/MCO/categories' # A resource example like items, search, category, etc.
        access_token = 'APP_USR-5052533537567494-081211-73dc630197472657716ff0d935be6123-1167652302' # Your access token.

    try:
        # Resource path GET
        # Request Access Token
        #api_response = api_instance.get_token(grant_type=grant_type, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, code=code, refresh_token=refresh_token)
        #pprint(api_response)
        api_response = api_instance.resource_get(resource, access_token)
        pprint(api_response)

        columns = ['id','name']
        
        with open('categories.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = columns)
            writer.writeheader()
            writer.writerows(api_response)



    except ApiException as e:
        print("Exception when calling OAuth20Api->get_token: %s\n" % e)