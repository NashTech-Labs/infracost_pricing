import json
import requests

filename = "example_json.json"
with open(filename, 'r+') as json_file:
    jsonfile_data = json.load(json_file)

    vendorname= jsonfile_data["resourcefilter"]["vendorName"]
    service = jsonfile_data["resourcefilter"]["service"]
    productfamily= jsonfile_data["resourcefilter"]["productFamily"]
    region = jsonfile_data["resourcefilter"]["region"]
    purchaseoption = jsonfile_data["pricefilter"]["purchaseOption"]
    currency = jsonfile_data["currency"]
    query1 = '''
  <
    products(
    filter: <
      vendorName: "{vendorname}",
      service: "{service}",
      productFamily: "{productfamily}",
      region: "{region}",
    '''.format(vendorname=vendorname, service=service, productfamily=productfamily, region=region)

    attributequery1 = '''
      attributeFilters: [
      '''
    attributequery2 = ''']
    >,
    ) 
   '''
    attribute_template = '< key: "{key}", value: "{value}" >,'
    for attribute in jsonfile_data["resourcefilter"]["attributeFilters"]:
      for key,value in attribute.items():
        attributequery1 = attributequery1 + attribute_template.format(key=key,value=value)

    query2 = attributequery1 + attributequery2

    
    query3 = '''<
    prices(
      filter: <
        purchaseOption: "{purchaseoption}"
      >,
    ) < {currency} >
  >
>
  '''.format(purchaseoption=purchaseoption,currency=currency)

    query = query1 + query2 + query3
    query = query.replace("<", "{").replace(">", "}") 
    #the brackets change as per graphql format 

    headers = {
    'X-Api-Key': 'ico-EeDdSfctrmjD14f45f45te5gJ7l6qw4o6M36sXT67a6',
    'Content-Type': 'application/json',
    }
    json_data = { 'query':query}

    response = requests.post(
    'https://pricing.api.infracost.io/graphql', headers=headers, json=json_data)

    print(json.dumps(response.json(), indent=4))  