import json
from typing import List, Dict

class Database:
    def __init__(self, db_path: str = './DATA.json'):
        self.db_path = db_path

    def load_data(self):
        try:
            with open(self.db_path, 'r') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = []

    def save_data(self, products: List[Dict]):
        self.data = products
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def extend_data(self, products: List[Dict]):
        self.load_data()
        self.data.extend(products)
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def update_if_needed(self, new_products: List[Dict]):
        self.load_data()
        for product in new_products:
            for existing in self.data:
                if existing['path_to_image'] == product['path_to_image']:
                    if existing['product_price'] != product['product_price']:
                        existing.update(product)
                    break
            else:
                self.data.append(product)
        self.save_data(self.data)
