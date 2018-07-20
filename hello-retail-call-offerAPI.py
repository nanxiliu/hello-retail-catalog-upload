from botocore.vendored import requests

def lambda_handler(event, context):
    for record in event["Records"]:
        print ("Recieved styleID in second lambda!")
        style_id = record["body"]
        print ("Style ID: ", record["body"])
       
        # api-endpoint
        URL = "" + style_id
         
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'apikey': ''}
        HEADERS = {'Accept': '', 'TraceContext': ''}
        # sending get request and saving the response as response object
        r = requests.get(url = URL, params = PARAMS, headers = HEADERS)
         
        # extracting data in json format
        data = r.json()

        gender = data["Product"]["Gender"]["Name"]
        product_type = data["Product"]["IMSProductType"]["DisplayName"]

        name = data["Product"]["PlainName"]
        brand = data["Product"]["Brand"]["DisplayName"]
        description = data["Product"]["Description"]

        if gender == "Female":
            category = "Women's " + product_type
        elif gender == "Male":
            category = "Men's" + product_type
        else:
            category = product_type

        print('Name: ', name)
        print('Brand: ', brand)
        print('Description: ', description)
        print('Category: ', category)
