class Product:

    def __init__(self, upc = None, p_name = None, p_desc = None, p_url = None):
        self.upc = upc
        self.p_name = p_name
        self.p_desc = p_desc
        self.p_url = p_url

class Item:
    def __init__(self, item_id = None, upc = None, quantity = None, expires = None):
        self.item_id = item_id
        self.upc = upc
        self.quantity = quantity
        self.expires = expires

class Data:
     def __init__(self, item_id = None, p_name = None, quantity = None, expires = None,  p_url = None):
         self.item_id = item_id
         self.p_name = p_name
         self.quantity = quantity
         self.expires = expires
         self.p_url = p_url