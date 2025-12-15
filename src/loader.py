import collections
import pandas as pd

class DataLoader:

    def load_orders(self):
        try:
            orders = pd.read_csv("data/orders.csv")
        except FileNotFoundError:
            raise FileNotFoundError("Order file not found")

        copy_orders = orders.copy()
        expected_columns = ['OrderID','ProductCode','Quantity','OrderDate','Priority']

        if (collections.Counter(list(copy_orders.columns)) != collections.Counter((expected_columns))):
            raise ValueError(f"Mismatched columns. Expected: {expected_columns}, found: {list(copy_orders.columns)}")
        
        if copy_orders.isnull().any().any():
            raise ValueError("Missing value found")
        
        if not copy_orders['OrderID'].is_unique:
            raise ValueError("OrderID must be unique")
        
        if (copy_orders['Quantity'] <= 0).any():
            raise ValueError("Quantity cannot be zero or negative")
        
        valid_priorities = {'urgent', 'normal'}
        priorities_lower = copy_orders['Priority'].str.lower()
        copy_orders['Priority'] = priorities_lower
        if not copy_orders['Priority'].isin(valid_priorities).all():
            raise ValueError("Invalid Priority found. Must be 'Urgent' or 'Normal'")
        
        copy_orders['OrderDate'] = pd.to_datetime(copy_orders['OrderDate'],errors = 'coerce')
        
        return copy_orders


    def load_inventory(self):
        try:
            inventory = pd.read_csv("data/inventory.csv")
        except FileNotFoundError:
            raise FileNotFoundError("Inventory file not found")
        
        copy_inventory = inventory.copy()
        expected_columns = ['ProductCode','AvailableStock']

        if (collections.Counter(list(copy_inventory.columns)) != collections.Counter(expected_columns)):
            raise ValueError(f"Mismatched columns expected: {expected_columns}, found: {list(copy_inventory.columns)}")
        
        if copy_inventory.isnull().any().any():
            raise ValueError("Missing value found")
        
        if not copy_inventory['ProductCode'].is_unique:
            raise ValueError("Product code must be unique")
        
        if (copy_inventory['AvailableStock'] < 0).any():
            raise ValueError("Available stock cannot be negative")
        
        return copy_inventory
        





