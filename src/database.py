import sqlite3
import pandas as pd
import os

def init_sqlite_db(data_dir="data"):
    """Loads CSV files into an in-memory SQLite database for fast SQL tool execution."""
    conn = sqlite3.connect(":memory:")
    
    csv_files = {
        "products": "products.csv",
        "categories": "categories.csv",
        "customers": "customers.csv",
        "orders": "orders.csv",
        "order_items": "order_items.csv",
        "promotions": "promotions.csv"
    }
    
    for table_name, filename in csv_files.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            df.to_sql(table_name, conn, index=False, if_exists="replace")
            
    return conn