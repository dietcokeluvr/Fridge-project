import urllib.request
import json
import pprint

from urllib.request import Request, urlopen

class API:
    def get_prod(self, upc):

        product_code = upc
        api_key = '4a41251085ccdb9bdc74069b5d2320d6a9723b26fa1f034743a47c1a968b28b9'

        req = Request('https://go-upc.com/api/v1/code/' + product_code)
        req.add_header('Authorization', 'Bearer ' + api_key)

        content = urlopen(req).read()
        data = json.loads(content.decode())

        product_name = data["product"]["name"]
        product_description = data["product"]["description"]
        product_image = data["product"]["imageUrl"]

        print("Product Name: " + product_name + "\n")
        print("Product Description: " + product_description + "\n")
        print("Product Image URL: " + product_image + "\n")
    

        




        






