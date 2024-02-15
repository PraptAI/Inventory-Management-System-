import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3


class Product:
    def __init__(self, product_id, name, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity


class InventoryManagementSystem:
    def __init__(self, db_filename="inventory.db"):
        self.db_filename = db_filename
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock_quantity INTEGER NOT NULL
                )
            """
            )

    def add_product(self, product):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO products (name, price, stock_quantity) VALUES (?, ?, ?)
            """,
                (product.name, product.price, product.stock_quantity),
            )
            conn.commit()
            print(f"Product '{product.name}' added successfully!")

    def update_product(self, product_id, new_details):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE products SET name=?, price=?, stock_quantity=? WHERE product_id=?
            """,
                (
                    new_details["name"],
                    new_details["price"],
                    new_details["stock_quantity"],
                    product_id,
                ),
            )
            conn.commit()
            print(f"Product updated successfully!")

    def remove_product(self, product_id):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM products WHERE product_id=?
            """,
                (product_id,),
            )
            conn.commit()
            print("Product removed successfully.")

    def get_product(self, product_id):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM products WHERE product_id=?
            """,
                (product_id,),
            )
            return cursor.fetchone()

    def track_stock(self, low_stock_threshold=10):
        products = self.get_products()
        low_stock_products = [
            p for p in products if p.stock_quantity < low_stock_threshold
        ]

        if low_stock_products:
            print("Low stock products:")
            for product in low_stock_products:
                print(f"{product.name}: {product.stock_quantity} units remaining")
                messagebox.showwarning(
                    "Low Stock",
                    f"Low stock for {product.name}. Quantity: {product.stock_quantity}",
                )
        else:
            print("All products are adequately stocked.")

    def record_sale(self, product_id, quantity):
        product = self.get_product(product_id)

        if product:
            if product[3] >= quantity:
                new_stock_quantity = product[3] - quantity
                with sqlite3.connect(self.db_filename) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        UPDATE products SET stock_quantity=? WHERE product_id=?
                    """,
                        (new_stock_quantity, product_id),
                    )
                    conn.commit()
                print(f"Sale recorded for '{product[1]}'. {quantity} units sold.")
            else:
                print(f"Insufficient stock for '{product[1]}'. Sale not recorded.")
        else:
            print("Product not found.")

    def generate_report(self):
        products = self.get_products()
        print("Sales Report:")
        for product in products:
            print(
                f"{product.name}: {product.stock_quantity} units sold: {product.stock_quantity - product.stock_quantity} units"
            )

    def get_products(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM products
            """
            )
            return [Product(*row) for row in cursor.fetchall()]


class InventoryManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Inventory Management System")

        # Initialize Inventory Management System
        self.inventory_system = InventoryManagementSystem()

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Labels with styles
        tk.Label(
            self.master,
            text="Product Management",
            font=("Helvetica", 16, "bold"),
            fg="blue",
        ).grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="n")
        tk.Label(self.master, text="Product ID:", font=("Arial", 12), fg="black").grid(
            row=1, column=0, pady=(5, 0), sticky="e"
        )
        tk.Label(
            self.master, text="Product Name:", font=("Arial", 12), fg="black"
        ).grid(row=2, column=0, pady=(5, 0), sticky="e")
        tk.Label(self.master, text="Price:", font=("Arial", 12), fg="black").grid(
            row=3, column=0, pady=(5, 0), sticky="e"
        )
        tk.Label(
            self.master, text="Stock Quantity:", font=("Arial", 12), fg="black"
        ).grid(row=4, column=0, pady=(5, 0), sticky="e")

        # Entry widgets with styles and increased size
        self.product_id_entry = tk.Entry(
            self.master, font=("Arial", 12), fg="blue", width=30
        )
        self.product_id_entry.grid(row=1, column=1, sticky="w")
        self.product_name_entry = tk.Entry(
            self.master, font=("Arial", 12), fg="blue", width=30
        )
        self.product_name_entry.grid(row=2, column=1, sticky="w")
        self.price_entry = tk.Entry(
            self.master, font=("Arial", 12), fg="blue", width=30
        )
        self.price_entry.grid(row=3, column=1, sticky="w")
        self.stock_quantity_entry = tk.Entry(
            self.master, font=("Arial", 12), fg="blue", width=30
        )
        self.stock_quantity_entry.grid(row=4, column=1, sticky="w")

    def add_product(self):
        try:
            name = self.product_name_entry.get()
            price = float(self.price_entry.get())
            stock_quantity = int(self.stock_quantity_entry.get())

            new_product = Product(
                len(self.inventory_system.get_products()) + 1,
                name,
                price,
                stock_quantity,
            )
            self.inventory_system.add_product(new_product)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter valid numeric values for Price and Stock Quantity.",
            )

    def update_product(self):
        try:
            product_id = int(self.product_id_entry.get())
            new_details = {
                "name": self.product_name_entry.get(),
                "price": float(self.price_entry.get()),
                "stock_quantity": int(self.stock_quantity_entry.get()),
            }

            self.inventory_system.update_product(product_id, new_details)

        except (ValueError, TypeError):
            messagebox.showerror("Error", "Please enter a valid numeric Product ID.")

    def remove_product(self):
        try:
            product_id = int(self.product_id_entry.get())
            self.inventory_system.remove_product(product_id)

        except (ValueError, TypeError):
            messagebox.showerror("Error", "Please enter a valid numeric Product ID.")

    def generate_report(self):
        self.inventory_system.generate_report()

    def track_stock(self):
        self.inventory_system.track_stock()

    def record_sale(self):
        try:
            product_id = int(self.product_id_entry.get())
            quantity = simpledialog.askinteger("Record Sale", "Enter quantity sold:")

            if quantity is not None:
                self.inventory_system.record_sale(product_id, quantity)

        except (ValueError, TypeError):
            messagebox.showerror(
                "Error",
                "Please enter valid numeric values for Product ID and Quantity.",
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementApp(root)

    root.geometry("400x500+300+200")  # Adjust the size and position as needed

    # Center the window on the screen
    root.geometry(
        "+%d+%d"
        % (
            (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2,
            (root.winfo_screenheight() - root.winfo_reqheight()) / 2,
        )
    )

    add_button = tk.Button(
        root,
        text="Add Product",
        command=app.add_product,
        bg="green",
        fg="white",
        font=("Arial", 14, "bold"),
        height=2,
        width=15,
    )
    add_button.grid(row=5, column=0, padx=10, pady=5, sticky="nsew")

    update_button = tk.Button(
        root,
        text="Update Product",
        command=app.update_product,
        bg="blue",
        fg="white",
        font=("Arial", 14, "bold"),
        height=2,
        width=15,
    )
    update_button.grid(row=5, column=1, padx=10, pady=5, sticky="nsew")

    remove_button = tk.Button(
        root,
        text="Remove Product",
        command=app.remove_product,
        bg="red",
        fg="white",
        font=("Arial", 14, "bold"),
        height=2,
        width=15,
    )
    remove_button.grid(row=6, column=0, padx=10, pady=5, sticky="nsew")

    report_button = tk.Button(
        root,
        text="Generate Report",
        command=app.generate_report,
        bg="orange",
        fg="white",
        font=("Arial", 14, "bold"),
        height=2,
        width=15,
    )
    report_button.grid(row=6, column=1, padx=10, pady=5, sticky="nsew")

    track_button = tk.Button(
        root,
        text="Track Stock",
        command=app.track_stock,
        bg="purple",
        fg="white",
        font=("Arial", 14, "bold"),
        height=2,
        width=15,
    )
    track_button.grid(row=7, column=0, padx=10, pady=5, sticky="nsew")

    sale_button = tk.Button(
        root,
        text="Record Sale",
        command=app.record_sale,
        bg="brown",
        fg="white",
        font=("Arial", 14, "bold"),
        height=2,
        width=15,
    )
    sale_button.grid(row=7, column=1, padx=10, pady=5, sticky="nsew")

    root.mainloop()
