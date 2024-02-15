import datetime


class Product:
    def __init__(self, product_id, name, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity


class InventoryManagementSystem:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)
        print(f"Product '{product.name}' added successfully!")

    def update_product(self, product_id, new_details):
        for product in self.products:
            if product.product_id == product_id:
                product.__dict__.update(new_details)
                print(f"Product '{product.name}' updated successfully!")
                return
        print("Product not found.")

    def remove_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                self.products.remove(product)
                print(f"Product '{product.name}' removed successfully!")
                return
        print("Product not found.")

    def track_stock(self):
        low_stock_threshold = 10
        low_stock_products = [
            p for p in self.products if p.stock_quantity < low_stock_threshold
        ]

        if low_stock_products:
            print("Low stock products:")
            for product in low_stock_products:
                print(f"{product.name}: {product.stock_quantity} units remaining")
        else:
            print("All products are adequately stocked.")

    def record_sale(self, product_id, quantity):
        for product in self.products:
            if product.product_id == product_id:
                if product.stock_quantity >= quantity:
                    product.stock_quantity -= quantity
                    print(f"Sale recorded for '{product.name}'. {quantity} units sold.")
                    return
                else:
                    print(
                        f"Insufficient stock for '{product.name}'. Sale not recorded."
                    )
                    return
        print("Product not found.")

    def generate_report(self):
        # Example: Print a simple report with product names and quantities
        print("Inventory Report:")
        for product in self.products:
            print(f"{product.name}: {product.stock_quantity} units")


if __name__ == "__main__":
    inventory_system = InventoryManagementSystem()

    # Adding products
    product1 = Product(1, "Laptop", 1000, 20)
    product2 = Product(2, "Printer", 200, 5)

    inventory_system.add_product(product1)
    inventory_system.add_product(product2)

    # Updating product details
    inventory_system.update_product(1, {"price": 1200, "stock_quantity": 25})

    # Recording a sale
    inventory_system.record_sale(1, 2)

    # Tracking stock
    inventory_system.track_stock()

    # Generating a report
    inventory_system.generate_report()
