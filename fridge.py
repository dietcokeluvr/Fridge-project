import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication,
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, QComboBox,
    QLineEdit, QPushButton, QMessageBox,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QStackedWidget, QStackedLayout
)
from PyQt6.QtCore import Qt
from Product_Item import Product, Item, Data
from database import DB
from themes import Theme
import urllib.request
import json
import pprint

from urllib.request import Request, urlopen

from Get_API import API


class MainWindow(QMainWindow):
       
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Fridge Application")

        self.fridgeList = []

        #Widgets for stacking bottom layout
        self.stackData = QWidget()
        self.stackProduct = QWidget()
        self.stackItem = QWidget()

        self.stackDUI()
        self.stackPUI()
        self.stackIUI()

        self.Stack = QStackedLayout(self)
        self.Stack.addWidget(self.stackData)
        self.Stack.addWidget(self.stackProduct)
        self.Stack.addWidget(self.stackItem)


############################################################################

        # tableLayout, Contains TableWidget
        tableLayout = QVBoxLayout()
        tableLayout.addWidget(QLabel("Products"))
        #############################################################################################################################
        self.tableView = QTableWidget() # QTableWidget
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # not allow edit directly to QTableWidget
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # select entire row when a cell in that row is selected
        self.tableView.verticalHeader().setVisible(False) # hide vertical header
        #############################################################################################################################
        tableLayout.addWidget(self.tableView)
        self.tableView.itemSelectionChanged.connect(self.display_selected_record)

        #display Layout contains buttons to select table display/ change input layout
        selectLayout = QHBoxLayout()
        self.databaseButton = QPushButton("Show Database")
        self.productButton = QPushButton("Product Table")

        self.itemButton = QPushButton("Item Table")

        selectLayout.addWidget(self.databaseButton)
        self.databaseButton.clicked.connect(self.set_display_0)

        selectLayout.addWidget(self.productButton)
        self.productButton.clicked.connect(self.set_display_1)
        self.productButton.clicked.connect(DB)
        

        selectLayout.addWidget(self.itemButton)
        self.itemButton.clicked.connect(self.set_display_2)
    
      

        # bottomRightLayout, Contains Exit button
        bottomRightLayout = QHBoxLayout()
        #############################################################################################################################
        # theme selection implementation     
        bottomRightLayout.addWidget(QLabel("Theme Selector"))
        self.themeSelector = QComboBox()
        self.themeSelector.addItems(["Light", "Dark", "Dracula"])
        bottomRightLayout.addWidget(self.themeSelector)

        self.theme = Theme(self)
        self.themeSelector.currentIndexChanged.connect(self.theme.changeTheme)

        app.setStyle('Fusion')
        app.setStyleSheet(self.theme.lightMode())
        #############################################################################################################################

        bottomRightLayout.addStretch()
        self.exitButton = QPushButton("Exit")
        bottomRightLayout.addWidget(self.exitButton)
        self.exitButton.clicked.connect(self.exitApp)


        #Bottom Layout
        bottomLayout = QHBoxLayout()
        bottomLayout.addLayout(bottomRightLayout)

        # main layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(tableLayout)
        mainLayout.addLayout(selectLayout)
        mainLayout.addLayout(self.Stack)
        mainLayout.addLayout(bottomLayout)



        mainLayoutWidget = QWidget()
        mainLayoutWidget.setLayout(mainLayout)
        self.setCentralWidget(mainLayoutWidget)

        self.initialize_window()


#######Functions for UI of stacked layouts
    def stackDUI(self):
        layout = QVBoxLayout()
        self.stackData.setLayout(layout)

#Product UI layout
    def stackPUI(self):
        layout = QVBoxLayout()
        #product Label & QLineEdit
        productLayout = QHBoxLayout()
        productLayout.addWidget(QLabel("UPC: "))
        productLayout.addStretch()
        self.upc_edit = QLineEdit()
        self.upc_edit.setStyleSheet("border: black; \
                                            font-weight: bold;")
        self.upc_edit.setFixedWidth(109)
        self.upc_edit.setFixedHeight(20)
        productLayout.addWidget(self.upc_edit)

        #p_name Label & QLineEdit
        p_nameLayout = QHBoxLayout()
        p_nameLayout.addWidget(QLabel("Product Name: "))
        p_nameLayout.addStretch()
        self.p_name_edit = QLineEdit()
        p_nameLayout.addWidget(self.p_name_edit)

        #p_desc Label & QLineEdit
        p_descLayout = QHBoxLayout()
        p_descLayout.addWidget(QLabel("Product description: "))
        p_descLayout.addStretch()
        self.p_desc_edit = QLineEdit()
        p_descLayout.addWidget(self.p_desc_edit)

        #p_url Label & QLineEdit
        p_urlLayout = QHBoxLayout()
        p_urlLayout.addWidget(QLabel("Image URL: "))
        p_urlLayout.addStretch()
        self.p_url_edit = QLineEdit()
        p_urlLayout.addWidget(self.p_url_edit)

        #p_imgLayout = QHBoxLayout()
        #p_imgLayout.addWidget(QLabel)

        buttonsLayout = QHBoxLayout()
        #updateButton = QPushButton("Update Entry")
        #updateButton.clicked.connect(self.update_product)
        insertButton = QPushButton("Insert New record")
        insertButton.clicked.connect(self.add_product)
        deleteButton = QPushButton("Delete Selected Record")
        deleteButton.clicked.connect(self.delete_product)
        #buttonsLayout.addWidget(updateButton)
        buttonsLayout.addWidget(insertButton)
        buttonsLayout.addWidget(deleteButton)

    #Stack label and edit boxes
        layout.addLayout(productLayout)
        layout.addLayout(p_nameLayout)
        layout.addLayout(p_descLayout)
        layout.addLayout(p_urlLayout)
        layout.addLayout(buttonsLayout)

        self.stackProduct.setLayout(layout)


#Item UI Layout
    def stackIUI(self):
        layout = QVBoxLayout()
        #Item Label & QLineEdit
        itemLayout = QHBoxLayout()
        itemLayout.addWidget(QLabel("Item ID: "))
        itemLayout.addStretch()
        self.i_id_edit = QLineEdit()
        self.i_id_edit.setStyleSheet("border: black; \
                                            font-weight: bold;")
        self.i_id_edit.setFixedWidth(109)
        self.i_id_edit.setFixedHeight(20)
        itemLayout.addWidget(self.i_id_edit)
        #item upc and QlineEdit
        upcLayout = QHBoxLayout()
        upcLayout.addWidget(QLabel("Item upc: "))
        upcLayout.addStretch()
        self.item_upc_edit = QLineEdit()
        upcLayout.addWidget(self.item_upc_edit)
        
        quantityLayout = QHBoxLayout()
        quantityLayout.addWidget(QLabel("Item Quantity: "))
        quantityLayout.addStretch()
        self.item_quantity_edit = QLineEdit()
        quantityLayout.addWidget(self.item_quantity_edit)

        expiresLayout = QHBoxLayout()
        expiresLayout.addWidget(QLabel("Item expiration: "))
        expiresLayout.addStretch()
        self.item_expires_edit = QLineEdit()
        expiresLayout.addWidget(self.item_expires_edit)


        buttonsLayout = QHBoxLayout()
        #updateButton = QPushButton("Update Entry")
        #updateButton.clicked.connect(self.update_item)
        insertButton = QPushButton("Insert New record")
        insertButton.clicked.connect(self.add_item)
        deleteButton = QPushButton("Delete Selected Record")
        deleteButton.clicked.connect(self.delete_item)
        #buttonsLayout.addWidget(updateButton)
        buttonsLayout.addWidget(insertButton)
        buttonsLayout.addWidget(deleteButton)

        layout.addLayout(itemLayout)
        layout.addLayout(upcLayout)
        layout.addLayout(quantityLayout)
        layout.addLayout(expiresLayout)
        layout.addLayout(buttonsLayout)
        self.stackItem.setLayout(layout)

#function to change display
    def display(self, i):
        self.Stack.setCurrentIndex(i)

#functions to set value of index in display function
    def set_display_0(self):
        fridge_database = DB()
        data = fridge_database.get_join_data()
        self.fridgeList.clear()
        self.display(0)
        for x in data:
            s = Data(x[0], x[1], x[2], x[3],x[4])
            self.fridgeList.append(s)
            
        self.display_database()
        self.clear_entries()


    def set_display_1(self):
        fridge_database = DB()
        data = fridge_database.get_product_data()
        self.display(1)
        self.fridgeList.clear()
        for x in data:
            s = Product(x[0], x[1], x[2], x[3])
            self.fridgeList.append(s)
            
        self.display_product_table()
        self.clear_entries()
 

    def set_display_2(self):
        fridge_database = DB()
        data = fridge_database.get_item_data()
        self.display(2)
        self.fridgeList.clear()
        for x in data:
            s = Item(x[0], x[1], x[2], x[3])
            self.fridgeList.append(s)
            
        self.display_item_table() 
        self.clear_entries()



    # initialize window
    def initialize_window(self):


        self.set_display_0()

    # update shipment information when update button clicked
    def update_product(self):
        selected_row = self.tableView.currentRow()
        try:
            if selected_row != -1: # check if a row in table is selected
                upc = int(self.upc_edit.text())
                p_name = self.p_name_edit.text()
                p_desc = self.p_desc_edit.text()
                p_url = self.p_url_edit.text()
                

                updated_product = Product(upc, p_name, p_desc, p_url)
                self.fridgeList[selected_row] = updated_product

                # Update in the database
                fridge_database = DB()
                fridge_database.update_product(upc, p_name, p_desc, p_url)

                # Update Table Display
                self.display_product_table()
                QMessageBox.information(self, "Success", "product updated successfully.") # notification of successful task
        except:
            QMessageBox.critical(self, "Error", "Please select a product to update.")

#UPDATE ITEM
    def update_item(self):
        selected_row = int(self.tableView.currentRow())
        upc = self.item_upc_edit.text()        

        
        try:
            if selected_row != -1: # check if a row in table is selected
                item_id = int(self.i_id_edit.text())
                upc = int(self.upc_edit.text())
                quantity = int(self.item_quantity_edit.text())
                expires = str(self.item_expires_edit.text())

                updated_item = Item(item_id, upc, quantity, expires)
                self.fridgeList[selected_row] = updated_item

                if upc not in [shipment.upc for shipment in self.fridgeList]:
                    self.upc_edit = self.item_upc_edit.text()
                    self.add_product()

                # Update in the database
                fridge_database = DB()
                fridge_database.update_item(item_id, upc, quantity, expires)

                # Update Table Display
                self.display_item_table()
                QMessageBox.information(self, "Success", "item updated successfully.") # notification of successful task
        except:
                QMessageBox.critical(self, "Error", "Please select a item to update.")
        else:
            QMessageBox.critical(self, "Error", "Do not duplicate a item name.")
    

    # add new product to table and to database    
    def add_product(self):

        product_code = self.upc_edit.text()
        if len(product_code) > 7 and len(product_code) < 14:
            if product_code not in [str(shipment.upc) for shipment in self.fridgeList]:

                try:
                    api_key = '4a41251085ccdb9bdc74069b5d2320d6a9723b26fa1f034743a47c1a968b28b9'

                    req = Request('https://go-upc.com/api/v1/code/' + product_code)
                    req.add_header('Authorization', 'Bearer ' + api_key)

                    content = urlopen(req).read()
                    data = json.loads(content.decode())

                    p_name = data["product"]["name"]
                    p_desc = data["product"]["description"]
                    p_url = data["product"]["imageUrl"]   

                    new_product = Product(product_code, p_name, p_desc, p_url)
                    self.fridgeList.append(new_product)
                    self.upc_edit.setText(str(product_code))
                    self.display_product_table()
                                
                    # select the new shipment that was just added to table/database
                    new_product_row = len(self.fridgeList) - 1 # because list index start with 0
                    self.tableView.selectRow(new_product_row) # selecting the row of the new shipment in table

                    QMessageBox.information(self, "Success", "Product added successfully.") # notification of successful task
                    
                    # Save to database
                    fridge_database = DB()
                    fridge_database.add_product(product_code, p_name, p_desc, p_url)
                except ValueError:
                    QMessageBox.critical(self, "Error", "Value Error")
            else:
                QMessageBox.critical(self, "Error", "Requires New UPC")
        else:
            QMessageBox.critical(self, "Error", "Requires Valid UPC")

            ####################################################
 
    # add new Item to table and to database    
    def add_item(self):
        item_id = self.i_id_edit.text()
        item_upc = self.item_upc_edit.text()
        quantity = self.item_quantity_edit.text()
        expires = self.item_expires_edit.text()
            #############################################################################################################################
            # Find the maximum Location ID and increment it by 1
            # Go through each item in fridgeList and find the max number of location ID
            # Then add 1 to it to generate new location ID
        new_item_id = max([shipment.item_id for shipment in self.fridgeList], default=0) + 1 # auto generate shipment ID 
                #############################################################################################################################
        new_item = Item(new_item_id, item_upc, quantity, expires)
        self.fridgeList.append(new_item) # add new item to fridgeList
        self.i_id_edit.setText(str(new_item_id)) # set new shipment ID to the shipment line edit
        self.display_item_table()
                
             # select the new item that was just added to table/database
        new_item_row = len(self.fridgeList) - 1 # because list index start with 0
        self.tableView.selectRow(new_item_row) # selecting the row of the new item in table

        QMessageBox.information(self, "Success", "Item added successfully.") # notification of successful task                
            # Save to database
        fridge_database = DB()
        fridge_database.add_item(new_item_id, item_upc, quantity, expires)
        

    # delete shipment from table and database
    def delete_product(self):
        selected_indexes = self.tableView.selectedIndexes()
        if selected_indexes:
            current_row = selected_indexes[0].row() # return index of the entire row
            deleted_product = self.fridgeList.pop(current_row)
            upc = str(deleted_product.upc)

            # Delete from database
            fridge_database = DB()
            fridge_database.delete_product(upc)
            # notification for successful task
            QMessageBox.information(self, "Success", "Product deleted successfully.")
            self.display_product_table()
            self.clear_entries()
        else:
            QMessageBox.critical(self, "Error", "Please select a Product to delete.")

#delete item
    def delete_item(self):
        selected_indexes = self.tableView.selectedIndexes()
        if selected_indexes:
            current_row = selected_indexes[0].row() # return index of the entire row
            deleted_item = self.fridgeList.pop(current_row)
            i_id = str(deleted_item.item_id)

            # Delete from database
            fridge_database = DB()
            fridge_database.delete_item(i_id)
            # notification for successful task
            QMessageBox.information(self, "Success", "Item deleted successfully.")
            self.display_item_table()
            self.clear_entries()
        else:
            QMessageBox.critical(self, "Error", "Please select an Item to delete.")

    def display_selected_record(self):
        selected_row = self.tableView.currentRow() # indexing current row in QTableWidget
        #for displaying 5 fields of selected record
        index = self.Stack.currentIndex()

        if index == 0:
            record = self.fridgeList[selected_row]
        
        #for displaying 2 fields of selected record
        if index == 1 :
            record = self.fridgeList[selected_row]
            self.upc_edit.setText(str(record.upc))
            self.p_name_edit.setText(str(record.p_name))
            self.p_desc_edit.setText(str(record.p_desc))
            self.p_url_edit.setText(str(record.p_url))

        if index == 2 :
            record = self.fridgeList[selected_row]
            self.i_id_edit.setText(str(record.item_id))
            self.item_upc_edit.setText(str(record.upc))
            self.item_quantity_edit.setText(str(record.quantity))
            self.item_expires_edit.setText(str(record.expires))


    def display_database(self):
        self.tableView.setRowCount(len(self.fridgeList)) # adjusts the number of rows in the table widget based on the number of shipments
        self.tableView.setColumnCount(5)
        headers = ["Item ID", "Product Name", "Product Quantity", "Expiration Date", "Image URL"]
        self.tableView.setHorizontalHeaderLabels(headers)
        #############################################################################################################################
        # iterating over a sequence (such as a list) while keeping track of both the index and the item at that index.
        # use the index as the row indicator in table setItem command
        for i, shipment in enumerate(self.fridgeList):
            self.tableView.setItem(i, 0, QTableWidgetItem(str(shipment.item_id)))
            self.tableView.setItem(i, 1, QTableWidgetItem(str(shipment.p_name)))
            self.tableView.setItem(i, 2, QTableWidgetItem(str(shipment.quantity)))
            self.tableView.setItem(i, 3, QTableWidgetItem(str(shipment.expires)))
            self.tableView.setItem(i, 4, QTableWidgetItem(str(shipment.p_url)))
            
        #############################################################################################################################
    
    def display_product_table(self):
        self.tableView.setRowCount(len(self.fridgeList)) # adjusts the number of rows in the table widget based on the number of shipments
        self.tableView.setColumnCount(4)
        headers = ["UPC", "Product Name", "Product Description", "Image URL"]
        self.tableView.setHorizontalHeaderLabels(headers)
        #############################################################################################################################
        # iterating over a sequence (such as a list) while keeping track of both the index and the item at that index.
        # use the index as the row indicator in table setItem command
        for i, shipment in enumerate(self.fridgeList):
            self.tableView.setItem(i, 0, QTableWidgetItem(str(shipment.upc)))
            self.tableView.setItem(i, 1, QTableWidgetItem(str(shipment.p_name)))
            self.tableView.setItem(i, 2, QTableWidgetItem(str(shipment.p_desc)))
            self.tableView.setItem(i, 3, QTableWidgetItem(str(shipment.p_url)))
            
        #############################################################################################################################           
        #############################################################################################################################
    
    def display_item_table(self):
        self.tableView.setRowCount(len(self.fridgeList)) # adjusts the number of rows in the table widget based on the number of shipments
        self.tableView.setColumnCount(4)
        headers = ["Item ID", "UPC", "Quantity", "Expiration Date"]
        self.tableView.setHorizontalHeaderLabels(headers)
        #############################################################################################################################
        # iterating over a sequence (such as a list) while keeping track of both the index and the item at that index.
        # use the index as the row indicator in table setItem command
        for i, shipment in enumerate(self.fridgeList):
            self.tableView.setItem(i, 0, QTableWidgetItem(str(shipment.item_id)))
            self.tableView.setItem(i, 1, QTableWidgetItem(str(shipment.upc)))
            self.tableView.setItem(i, 2, QTableWidgetItem(str(shipment.quantity)))
            self.tableView.setItem(i, 3, QTableWidgetItem(str(shipment.expires)))

            
        ###########################################################################################################################    
    
    # clear data in QlineEdit
    def clear_entries(self):
        self.p_desc_edit.clear()
        self.p_name_edit.clear()
        self.p_url_edit.clear()
        self.item_expires_edit.clear()
        self.item_quantity_edit.clear()
        self.i_id_edit.clear()
        self.item_upc_edit.clear()

    # exit button
    def exitApp(self):
        self.close()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()        
