import sys
import urllib.request
import json
from PyQt6.QtWidgets import (QMainWindow, QApplication, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QListWidget, QListWidgetItem, QMessageBox)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel
from database import DB


class BarcodeScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Barcode Scanner")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Styling
        self.central_widget.setStyleSheet("background-color: #F0F0F0; font-size: 14px;")

        # Left layout for inputs and buttons
        self.leftLayout = QVBoxLayout()
        self.layout.addLayout(self.leftLayout)

        # Right layout for displaying details and image
        self.rightLayout = QVBoxLayout()
        self.layout.addLayout(self.rightLayout)

        # Barcode entry
        self.barcodeEntryLayout = QHBoxLayout()
        self.leftLayout.addLayout(self.barcodeEntryLayout)
        self.label = QLabel("Scan a barcode:")
        self.barcodeEntryLayout.addWidget(self.label)
        self.entry = QLineEdit()
        self.entry.setStyleSheet("background-color: white;")
        self.barcodeEntryLayout.addWidget(self.entry)

        # Manual entry and see details button
        self.manualEntryLayout = QHBoxLayout()
        self.leftLayout.addLayout(self.manualEntryLayout)
        self.manualEntry = QLineEdit()
        self.manualEntry.setPlaceholderText("Enter barcode manually")
        self.manualEntry.setStyleSheet("background-color: white;")
        self.manualEntryLayout.addWidget(self.manualEntry)
        self.seeDetailsButton = QPushButton("See Details")
        self.seeDetailsButton.clicked.connect(self.fetch_product_details_from_api)
        self.manualEntryLayout.addWidget(self.seeDetailsButton)

        # Product details display
        self.productDetails = QListWidget()
        self.productDetails.setStyleSheet("background-color: white;")
        self.rightLayout.addWidget(self.productDetails)

        # Product image display
        self.productImageLabel = QLabel()
        self.rightLayout.addWidget(self.productImageLabel)

        # View Fridge button
        self.viewFridgeButton = QPushButton("View Fridge")
        self.viewFridgeButton.clicked.connect(self.view_fridge)
        self.leftLayout.addWidget(self.viewFridgeButton)

        # Add Item button
        self.addItemButton = QPushButton("Add Item")
        self.addItemButton.clicked.connect(self.add_item)
        self.leftLayout.addWidget(self.addItemButton)

    def fetch_product_details_from_api(self):
        barcode = self.manualEntry.text()
        api_key = '4a41251085ccdb9bdc74069b5d2320d6a9723b26fa1f034743a47c1a968b28b9'
        req = urllib.request.Request(f'https://go-upc.com/api/v1/code/{barcode}')
        req.add_header('Authorization', 'Bearer ' + api_key)
        try:
            content = urllib.request.urlopen(req).read()
            data = json.loads(content.decode())
            product_name = data["product"]["name"]
            product_description = data["product"]["description"]
            product_image = data["product"]["imageUrl"]
            self.display_product_details(product_name, product_description, product_image)
        except Exception as e:
            self.productDetails.clear()
            self.productDetails.addItem("Failed to fetch details or Barcode not valid.")

    def display_product_details(self, name, description, image_url):
        self.productDetails.clear()
        self.productDetails.addItem(f"Name: {name}")
        self.productDetails.addItem(f"Description: {description}")
        self.productDetails.addItem(f"Image URL: {image_url}")

        image = QPixmap()
        image.loadFromData(urllib.request.urlopen(image_url).read())
        self.productImageLabel.setPixmap(image.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))

    '''-------------------------------------------------------------------------
    Type: AI Generated
    Attribution: ChatGPT 3.5
    Function: view fridge
    Prompt: create a view fridge function based on code
    Source: https://chat.openai.com/
-------------------------------------------------------------------------'''
    def view_fridge(self):
        # Placeholder for the functionality to view fridge contents
        db = DB()
        contents = db.get_item_data()
        if contents:
            self.productDetails.clear()
            self.productDetails.addItem("Fridge Contents:")
            for item in contents:
                item_id, expires, quantity, upc = item
                self.productDetails.addItem(f"Item ID: {item_id}, Expires: {expires}, Quantity: {quantity}, UPC: {upc}")
        else:
            self.productDetails.clear()
            self.productDetails.addItem("The fridge is empty.")

    '''-------------------------------------------------------------------------
    Type: AI Generated
    Attribution: ChatGPT 3.5
    Function: add item
    Prompt: create an add item function based on code
    Source: https://chat.openai.com/
-------------------------------------------------------------------------'''
    def add_item(self):
        # Placeholder for the functionality to add item to your inventory
        upc = self.entry.text()
        db = DB()
        product = db.get_item_data(upc)
        if product:
            db.add_product(upc, 1)  # Assuming quantity is always 1 for simplicity
            QMessageBox.information(self, "Success", "Item added to the fridge.")
        else:
            QMessageBox.warning(self, "Error", "Product not found. Please scan a valid barcode.")
        print("Item added to the inventory")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    barcode_app = BarcodeScannerApp()
    barcode_app.show()
    sys.exit(app.exec())

