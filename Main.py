import sys
from enum import Enum
from PyQt6.QtWidgets import (QMainWindow, QApplication,
    QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
import tkinter as tk
import keyboard

class BarcodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Barcode Scanner")
        
        self.label = tk.Label(root, text="Scan a barcode:")
        self.label.pack()
        
        self.barcode_var = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.barcode_var, state="disabled")
        self.entry.pack()
        
        self.item_name_var = tk.StringVar()
        self.item_name_label = tk.Label(root, text="Item Name:")
        self.item_name_label.pack()
        self.item_name_entry = tk.Entry(root, textvariable=self.item_name_var, state="disabled")
        self.item_name_entry.pack()
        
        self.expiration_date_var = tk.StringVar()
        self.expiration_date_label = tk.Label(root, text="Expiration Date:")
        self.expiration_date_label.pack()
        self.expiration_date_entry = tk.Entry(root, textvariable=self.expiration_date_var, state="disabled")
        self.expiration_date_entry.pack()
        
        self.start_scanning_button = tk.Button(root, text="Start Scanning", command=self.start_scanning)
        self.start_scanning_button.pack()
        
        self.stop_scanning_button = tk.Button(root, text="Stop Scanning", command=self.stop_scanning, state="disabled")
        self.stop_scanning_button.pack()
        
        self.barcode_var.trace_add("write", self.track_barcode)
        
        self.barcode_scanning = False

    def start_scanning(self):
        self.barcode_scanning = True
        self.entry.config(state="normal")
        self.entry.delete(0, "end")
        self.entry.focus()
        self.item_name_entry.config(state="normal")
        self.expiration_date_entry.config(state="normal")
        self.start_scanning_button.config(state="disabled")
        self.stop_scanning_button.config(state="normal")
        keyboard.on_release(self.check_for_barcode)

    def stop_scanning(self):
        self.barcode_scanning = False
        self.entry.delete(0, "end")
        self.entry.config(state="disabled")
        self.item_name_entry.delete(0, "end")
        self.item_name_entry.config(state="disabled")
        self.expiration_date_entry.delete(0, "end")
        self.expiration_date_entry.config(state="disabled")
        self.start_scanning_button.config(state="normal")
        self.stop_scanning_button.config(state="disabled")
        keyboard.unhook(self.check_for_barcode)

    def check_for_barcode(self, event):
        if self.barcode_scanning:
            if keyboard.is_pressed("enter"):
                self.stop_scanning()
                self.entry.delete(len(self.entry.get())-1, "end")

    def track_barcode(self, *args):
        barcode = self.barcode_var.get()
        item_name = self.item_name_var.get()
        expiration_date = self.expiration_date_var.get()
        print(f"Scanned barcode: {barcode}, Item: {item_name}, Expiration Date: {expiration_date}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BarcodeScannerApp(root)
    root.mainloop()

