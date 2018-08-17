from botocore.vendored import requests
import sys, os, base64, datetime, hashlib, hmac, json

# Define variables for HR eventwriter API call
method = 'POST'
service = 'execute-api'
# Replace API_ID with your API ID
host = 'API_ID' + '.execute-api.us-west-2.amazonaws.com'
region = 'us-west-2'
endpoint = 'https://ec2.amazonaws.com'

# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

# Have access key, secret key, and session token for AWS authentication
# TODO: Better to put these in a config file and not directly in code!
# Important: Need to run 'awscreds' in terminal then do 'sudo cat ~/.aws/credentials' then update 'access_key', 'secret_key', and 'session_token'

access_key = ""
secret_key = ""
session_token = ""

def lambda_handler(event, context):
    for record in event["Records"]:
        style_id = str(record["body"])
       
        # Call Offer API to get product info and image
        # Replace with correct url, params, and headers
        offer_url = ""
        offer_params = {}
        offer_headers = {}

        r = requests.get(url = offer_url, params = offer_params, headers = offer_headers)
        data = r.json()
        print ("Offer API Data: ", data)

        gender = data
        product_type = data
        
        if gender == "Female":
            category = "Women's " + product_type
        elif gender == "Male":
            category = "Men's " + product_type
        else:
            category = product_type

        # Replace with correct data
        name = data
        brand = data
        description = data
        image = data[8:] #to cut out https://

        print('Style ID: ', style_id)
        print('Name: ', name)
        print('Brand: ', brand)
        print('Description: ', description)
        print('Category: ', category)
        print('Image URL: ', image)
        
        # Replace with your API endpoint
        eventwriter_endpoint = ''
        merchant_data = ({
            "id": str(style_id),
            "name": str(name),
            "origin":"",
            "description": str(description),
            "schema":"com.nordstrom/product/create/1-0-0",
            "category": str(category),
            "brand": str(brand),
            "image": str(image),
        })
        
        # Create a date for headers and the credential string
        t = datetime.datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope
        
        # ************* TASK 1: CREATE A CANONICAL REQUEST *************
        # http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html
        canonical_uri = '/' 
        canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n' + 'x-amz-security-token:' + session_token + '\n'
        signed_headers = 'host;x-amz-date;x-amz-security-token'
        payload_hash = hashlib.sha256(json.dumps(merchant_data).encode('utf-8')).hexdigest()
        canonical_request = method + '\n' + '/boston/event-writer' + '\n\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
        
        # ************* TASK 2: CREATE THE STRING TO SIGN*************
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        
        # ************* TASK 3: CALCULATE THE SIGNATURE *************
        signing_key = getSignatureKey(secret_key, datestamp, region, service)
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

        # ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
        authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
        auth_headers = {'x-amz-date':amzdate, 'Authorization':authorization_header, 'x-amz-security-token': session_token}
        
        response = requests.post(eventwriter_endpoint, data=json.dumps(merchant_data), headers=auth_headers)
        data2 = response.json()
        
        print('Response: ', response)
        print('JSON Response: ', data2)
        
