# You need use this example code in to the main folder
from __future__ import print_function
import time
import meli
from meli.rest import ApiException
from pprint import pprint
import csv

def get_items_info():
    # Defining the host, defaults to https://api.mercadolibre.com
    # See configuration.py for a list of all supported configuration parameters.
    configuration = meli.Configuration(
        host = "https://api.mercadolibre.com"
    )


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
        #api_response = api_instance.resource_get(resource, access_token)
        #pprint(api_response)
        list_items = []
        with open('most_sold.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, skipinitialspace=True)
            for row in reader:
                if bool(row):
                    list_items.append(row)
            
        pprint(list_items)

        item_prices = []

        #get base price
        for list in list_items:
            api_instance = meli.RestClientApi(api_client)
            try:
                resourceA = '/items/'+list[0] # A resource example like items, search, category, etc.
                access_tokenA = 'APP_USR-5052533537567494-081211-73dc630197472657716ff0d935be6123-1167652302' # Your access token.
                api_item_resA = api_instance.resource_get(resourceA, access_tokenA)

                resourceB = '/reviews/item/'+list[0] # A resource example like items, search, category, etc.
                access_tokenB = 'APP_USR-5052533537567494-081211-73dc630197472657716ff0d935be6123-1167652302' # Your access token.
                api_item_resB = api_instance.resource_get(resourceB, access_tokenB)

                resourceC = '/visits/items?ids='+list[0] # A resource example like items, search, category, etc.
                access_tokenC = 'APP_USR-5052533537567494-081211-73dc630197472657716ff0d935be6123-1167652302' # Your access token.
                api_item_resC = api_instance.resource_get(resourceC, access_tokenC)

                aux_list = []
                aux_list.append(list[0])
                aux_list.append(api_item_resA['title'])
                aux_list.append(api_item_resA['base_price'])
                aux_list.append(api_item_resA['sold_quantity'])
                aux_list.append(api_item_resB['rating_average'])
                aux_list.append(api_item_resC[list[0]])
                item_prices.append(aux_list)

            except ApiException as e:
                pprint(e.reason)
                #pprint('no treatment for products')

        pprint(item_prices)

        columns = ['id','title','base_price','sold_quantity','rating_average','visits']
        item_dict = [dict(zip(columns, i)) for i in item_prices]

        with open('products_info.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = columns)
            writer.writeheader()
            writer.writerows(item_dict)

    except ApiException as e:
        print("Exception when calling OAuth20Api->get_token: %s\n" % e)