import pymysql
from datetime import date, timedelta

# Database connection
db = pymysql.connect(host="localhost", user="root", password="123456", database="smart_cart_db")
cursor = db.cursor()

# Sample products to insert
products = [
    ("P001", "Amul Milk 1L", 52.0, 100, date.today() + timedelta(days=10)),
    ("P002", "Parle-G Biscuits", 10.0, 200, date.today() + timedelta(days=180)),
    ("P003", "Colgate Toothpaste", 45.5, 150, date.today() + timedelta(days=365)),
    ("P004", "Surf Excel 500g", 85.0, 75, date.today() + timedelta(days=400)),
    ("P005", "Lays Chips", 20.0, 300, date.today() + timedelta(days=60))
]

# Insert products
for product in products:
    cursor.execute("""
        INSERT INTO products (product_id, name, price, quantity, expiry_date)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE name=VALUES(name), price=VALUES(price), quantity=VALUES(quantity), expiry_date=VALUES(expiry_date)
    """, product)

db.commit()
print("✅ Sample products added to the database.")
db.close()
