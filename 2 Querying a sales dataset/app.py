import sqlite3
import pandas as pd
import os

db_path = 'database/amazon.db'
csv_path = 'database/amazon.csv'

if not os.path.exists(db_path): 
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
   
    df = pd.read_csv(csv_path)

    
    df["actual_price"] = df["actual_price"].str.replace('₹', '').str.replace(',', '')  
    df["actual_price"] = df["actual_price"].astype(float)
    df["actual_price"] = df["actual_price"].apply(lambda x: x * 0.01)
    
    df["discounted_price"] = df["discounted_price"].str.replace('₹', '').str.replace(',', '')  
    df["discounted_price"] = df["discounted_price"].astype(float)
    df["discounted_price"] = df["discounted_price"].apply(lambda x: x * 0.01)
  
    df.to_sql('sales', conn, if_exists='replace', index=False)
   
    conn.close()

    print("Database created successfully!")




# Most Expensive Products
def most_expensive_products():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    command = """
    SELECT product_name, actual_price
    FROM sales 
    GROUP BY product_name
    ORDER BY actual_price DESC
    LIMIT 5

    """
    c.execute(command)

    rows = c.fetchall()
    for row in rows:
        print(f"{row[0]} - ${row[1]:.2f}")
    conn.close()

#Best Selling Categories
def best_selling_categories():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    command = """
    SELECT category, SUM(actual_price) AS price_sum
    FROM sales 
    GROUP BY category
    ORDER BY price_sum DESC
    LIMIT 5

    """
    c.execute(command)

    rows = c.fetchall()
    for row in rows:
        print(f"{row[0].split("|")[-1]} - ${row[1]:.2f}")
    conn.close()

# Categories with most products
def categories_with_most_products():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    command = """
    SELECT category, COUNT(*) AS product_count
    FROM sales
    GROUP BY category
    ORDER BY product_count DESC
    LIMIT 5
    """
    c.execute(command)

    rows = c.fetchall()
    for row in rows:
        print(f"{row[0].split("|")[-1]} - ({row[1]:.0f})")
    

    conn.close()

# cheaper products
def cheaper_products():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    command2 = """
    SELECT product_name, actual_price
    FROM sales
    WHERE CAST(actual_price AS REAL) > 0
    AND CAST(actual_price AS REAL) <= 100
    ORDER BY CAST(actual_price AS REAL) ASC    
    LIMIT 5
    """
    command = """
    SELECT product_name, actual_price
    FROM sales
    WHERE  actual_price > 0
    AND actual_price <= 100
    ORDER BY actual_price ASC    
    LIMIT 5
    """
    c.execute(command)

    rows = c.fetchall()
    for row in rows:
        print(f"{row[0]} - ({row[1]:.2f})")
    

    conn.close()

print("#"*20,"More Expensive","#"*20 + "\n")
most_expensive_products()
print("\n")

print("#"*20,"Best Selling Categories","#"*20 + "\n")
best_selling_categories()
print("\n")

print("#"*20,"Categories with most products","#"*20 + "\n")
categories_with_most_products()
print("\n")

print("#"*20,"Cheaper Products","#"*20 + "\n")
cheaper_products()
print("\n")

