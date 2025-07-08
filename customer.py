import pymysql

# Connect to MySQL
db = pymysql.connect(host="localhost", user="root", password="123456", database="smart_cart_db")
cursor = db.cursor()

# Simulate LCD output
def lcd_display(message):
    print("\n[ LCD DISPLAY ]")
    print(message)
    print("[ ------------- ]\n")

# Start/Reuse cart
def activate_cart(cart_id):
    cursor.execute("SELECT status FROM carts WHERE cart_id = %s", (cart_id,))
    result = cursor.fetchone()

    if result:
        if result[0] == 'checked_out':
            # clear old items for reuse
            cursor.execute("DELETE FROM cart_items WHERE cart_id = %s", (cart_id,))
            cursor.execute("UPDATE carts SET status = 'in_use' WHERE cart_id = %s", (cart_id,))
            db.commit()
        elif result[0] == 'in_use':
            print(f"🔄 Cart {cart_id} already in use. Continuing session.")
        else:
            cursor.execute("UPDATE carts SET status = 'in_use' WHERE cart_id = %s", (cart_id,))
            db.commit()
    else:
        cursor.execute("INSERT INTO carts (cart_id, status) VALUES (%s, 'in_use')", (cart_id,))
        db.commit()

# Scan product
def scan_product(cart_id, barcode, quantity=1):
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (barcode,))
    product = cursor.fetchone()

    if not product:
        lcd_display("❌ Product not found.")
        return

    # Display info on LCD
    lcd_message = (
        f"Product ID: {product[1]}\n"      # product_id
        f"Name: {product[2]}\n"            # name
        f"Price: ₹{product[3]}\n"          # price
        f"Qty: {quantity}\n"               # quantity entered by user
        f"Expiry: {product[5]}"            # expiry_date
    )
    lcd_display(lcd_message)

    # Check if item already in cart
    cursor.execute("""
        SELECT quantity FROM cart_items
        WHERE cart_id = %s AND product_id = %s
    """, (cart_id, barcode))
    existing = cursor.fetchone()

    if existing:
        # If item exists, update quantity
        new_qty = existing[0] + quantity
        cursor.execute("""
            UPDATE cart_items
            SET quantity = %s
            WHERE cart_id = %s AND product_id = %s
        """, (new_qty, cart_id, barcode))
    else:
        # Else insert new
        cursor.execute("""
            INSERT INTO cart_items (cart_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """, (cart_id, barcode, quantity))

    db.commit()
    print("✅ Added to cart.")

# Simulate customer session
def customer_session(cart_id):
    activate_cart(cart_id)

    print(f"🛒 Smart Cart Session Started — Cart ID: {cart_id}")
    while True:
        barcode = input("Scan product barcode (or type 'done' to finish): ")
        if barcode.lower() == 'done':
                      # Show total bill before exiting
            cursor.execute("""
                SELECT p.name, ci.quantity, p.price, (ci.quantity * p.price) AS total
                FROM cart_items ci
                JOIN products p ON ci.product_id = p.product_id
                WHERE ci.cart_id = %s
            """, (cart_id,))
            items = cursor.fetchall()

            if items:
                print("\n🧾 CART TOTAL (on LCD):")
                grand_total = 0
                for item in items:
                    name, qty, price, total = item
                    print(f"{name} x {qty} @ ₹{price} = ₹{total}")
                    grand_total += total
                print(f"💰 Total: ₹{grand_total}")
            else:
                print("🛒 Cart is empty.")

            print("🔒 Cart session ended. Proceed to checkout.")
            break
        scan_product(cart_id, barcode, quantity=1)

# Run cart code
if __name__ == "__main__":
    cart_id = input("Enter your Cart ID (e.g. CART001): ").strip().upper()
    customer_session(cart_id)
