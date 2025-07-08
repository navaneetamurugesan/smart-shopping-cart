import pymysql

# Connect to DB
db = pymysql.connect(host="localhost", user="root", password="123456", database="smart_cart_db")
cursor = db.cursor()

def checkout_cart(cart_id):
    # Check cart status
    cursor.execute("SELECT status FROM carts WHERE cart_id = %s", (cart_id,))
    result = cursor.fetchone()

    if not result:
        print("❌ Cart ID not found.")
        return

    if result[0] != 'in_use':
        print("❗ Cart is not in use or already checked out.")
        return

    # Fetch and summarize items
    cursor.execute("""
        SELECT p.name, SUM(ci.quantity), p.price, SUM(ci.quantity * p.price) AS total
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.product_id
        WHERE ci.cart_id = %s
        GROUP BY p.name, p.price
    """, (cart_id,))
    items = cursor.fetchall()

    if not items:
        print("🛒 Cart is empty.")
        return

    # Show bill
    print("\n🧾 Final Bill:")
    grand_total = 0
    for item in items:
        name, qty, price, total = item
        print(f"{name} x {qty} @ ₹{price} = ₹{total}")
        grand_total += total
    print(f"💰 Total: ₹{grand_total}\n")

    # Store summary bill in transactions table
    cursor.execute("""
        INSERT INTO checkout_summary (cart_id, total)
        VALUES (%s, %s)
    """, (cart_id, grand_total))

    # Clear cart and mark for reuse
    cursor.execute("DELETE FROM cart_items WHERE cart_id = %s", (cart_id,))
    cursor.execute("UPDATE carts SET status = 'checked_out' WHERE cart_id = %s", (cart_id,))
    db.commit()

    print(f"✅ Bill stored. Cart {cart_id} is now ready for reuse.")

# Main run
if __name__ == "__main__":
    print("=== Billing Counter ===")
    cart_id = input("Scan Cart ID: ").strip().upper()
    checkout_cart(cart_id)
