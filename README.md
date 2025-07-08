# smart-shopping-cart
This is a Python + MySQL-based Smart Shopping Cart System with barcode scanning, LCD simulation, cart ID tracking, and billing features.

## Features
- Scan products using barcode
- LCD-style display of product info
- Auto-cart clearing after billing
- Transaction log and cart reuse
- Admin-friendly database setup

## Tech Stack
- Python
- MySQL
- PyMySQL

## Usage
1. Run `load_products.py` to load sample products.
2. Use `customer.py` to simulate product scanning.
3. Use `worker.py` to checkout and generate bill.

## Setup
```bash
pip install pymysql
