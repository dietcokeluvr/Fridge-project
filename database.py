import sqlite3
import csv
# In Progress
class DB:
    
    def __init__(self):
        self.filename = "FridgeDB.db"
        self.csvProduct = "productCSV.csv"
        self.csvItem = "itemCSV.csv"
        
        table_name = self.get_table_name()
        if not "product" in table_name:
            self.create_product_table()
        if not "item" in table_name:
            self.create_item_table()

    # return table names in the database
    def get_table_name(self):
        con = sqlite3.connect(self.filename)
        cur = con.cursor() 
        res = cur.execute("SELECT name FROM sqlite_master") 
        table_names = [x[0] for x in res.fetchall()] 
        con.close()
        return table_names

    # create the product table
    def create_product_table(self):
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        sqlstr = "CREATE TABLE product (upc	INTEGER NOT NULL UNIQUE, p_name	TEXT NOT NULL,\
                  p_desc TEXT, p_url TEXT, PRIMARY KEY(upc));"
        
        res = cur.execute(sqlstr)

        data = []
        with open(self.csvProduct, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for x in csvreader:
                x[0] = int(x[0])
                row = tuple(x)    
                data.append(row)
            print("%d rows read."%(csvreader.line_num))
            cur.executemany("INSERT INTO Shipment VALUES (?, ?, ?, ?)", data)
            con.commit()
            con.close()

    # create the item table
    def create_item_table(self):
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        sqlstr = "CREATE TABLE item (item_id INTEGER NOT NULL UNIQUE, expires TEXT, \
	                quantity INTEGER, upc INTEGER NOT NULL,\
	                FOREIGN KEY(upc) REFERENCES product(upc) ON DELETE CASCADE, \
	                PRIMARY KEY(itemID AUTOINCREMENT));"
        
        res = cur.execute(sqlstr)

        data = []
        with open(self.csvItem, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for x in csvreader:
                x[0] = int(x[0])
                row = tuple(x)    
                data.append(row)
            print("%d rows read."%(csvreader.line_num))
            cur.executemany("INSERT INTO Item VALUES (?, ?)", data)
            con.commit()
            con.close()


    # Add a new product
    def add_product(self, upc, p_name, p_desc, p_url):
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        cur.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (upc, p_name, p_desc, p_url))
        con.commit()
        con.close()



    # Delete a shipment
    def delete_product(self, upc):
        
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        cur.execute("DELETE FROM product WHERE upc = " + upc)
        con.commit()
        con.close()

    # Delete a location
    def delete_location(self, location_id):
        
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        cur.execute("DELETE FROM Location WHERE location_id = " + location_id)
        con.commit()
        con.close()

    # Delete a item
    def delete_item(self, item_id):
        
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        cur.execute("DELETE FROM Item WHERE item_id = " + item_id)
        con.commit()
        con.close()

    #Show shipment table
    def get_shipment_data(self):
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        res = cur.execute("SELECT * FROM Shipment")
        data = res.fetchall()
        return data
    
    #Show item table
    def get_item_data(self):
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        res = cur.execute("SELECT * FROM Item")
        data = res.fetchall()
        return data
    
    #Show location table
    def get_location_data(self):
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        res = cur.execute("SELECT * FROM Location")
        data = res.fetchall()
        return data
    
    #show Joined tables
    def get_join_data(self):
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        res = cur.execute("SELECT Shipment.shipment_id, Location.location_name , Item.item_name, Shipment.quantity \
                FROM Shipment LEFT JOIN Location USING (location_id) \
                LEFT JOIN Item USING (item_id);")
        data = res.fetchall()
        return data
    
    
