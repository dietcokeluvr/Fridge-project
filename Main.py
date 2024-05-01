import sys
from enum import Enum
from PyQt6.QtWidgets import (QMainWindow, QApplication,
    QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox, QListView, QListWidget, QListWidgetItem,
)
from PyQt6.QtCore import Qt

class BarcodeScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Barcode Scanner")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)



        
        self.leftLayout = QVBoxLayout()
        self.layout.addLayout(self.leftLayout)

        self.rightLayout = QVBoxLayout()
        self.layout.addLayout(self.rightLayout)


        self.barcodeEntryLayout = QHBoxLayout()
        self.leftLayout.addLayout(self.barcodeEntryLayout)
        
        self.label = QLabel("Scan a barcode:")
        self.barcodeEntryLayout.addWidget(self.label)
        self.entry = QLineEdit()
        self.entry.setDisabled(False)
        self.barcodeEntryLayout.addWidget(self.entry)


        
        self.itemNameEntryLayout = QHBoxLayout()
        self.leftLayout.addLayout(self.itemNameEntryLayout)

        self.item_name_label = QLabel("Item Name:")
        self.itemNameEntryLayout.addWidget(self.item_name_label)
        self.item_name_entry = QLineEdit()
        self.item_name_entry.setDisabled(False)
        self.itemNameEntryLayout.addWidget(self.item_name_entry)


        self.expirationDateLayout = QHBoxLayout()
        self.leftLayout.addLayout(self.expirationDateLayout)

        self.expiration_date_label = QLabel("Expiration Date:")
        self.expirationDateLayout.addWidget(self.expiration_date_label)
        self.expiration_date_entry = QLineEdit()
        self.expiration_date_entry.setDisabled(False)
        self.expirationDateLayout.addWidget(self.expiration_date_entry)

    


        self.rightListViewLayout = QVBoxLayout()
        self.rightLayout.addLayout(self.rightListViewLayout)

        self.listView = QListView()
        self.rightListViewLayout.addWidget(self.listView)


        self.buttonLayout = QHBoxLayout()
        self.leftLayout.addLayout(self.buttonLayout)

        self.addItemButton = QPushButton(text="Add Item")
        self.addItemButton.clicked.connect(self.add_item)


        self.removeItem = QPushButton(text="Remove Item")
        self.removeItem.clicked.connect(self.remove_item)

        self.buttonLayout.addWidget(self.addItemButton)
        self.buttonLayout.addWidget(self.removeItem)


        self.barcode_scanning = False


    def check_for_barcode(self, text):
        if self.barcode_scanning and "\n" in text:
            self.stop_scanning()
            self.entry.setText(text[:-1])
            self.track_barcode()

    def track_barcode(self):
        barcode = self.entry.text()
        item_name = self.item_name_entry.text()
        expiration_date = self.expiration_date_entry.text()
        print(f"Scanned barcode: {barcode}, Item: {item_name}, Expiration Date: {expiration_date}")


    def add_item(self):
        print("add item")

    def remove_item(self):
        print("item removed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    barcode_app = BarcodeScannerApp()
    barcode_app.show()
    sys.exit(app.exec())