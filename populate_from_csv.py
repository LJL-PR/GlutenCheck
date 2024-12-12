import sqlite3
import pandas as pd

# Load the CSV file
csv_file_path = 'gluten_data.csv'
data = pd.read_csv(csv_file_path)

# Connect to the SQLite database
conn = sqlite3.connect('db/food_data.db')
cursor = conn.cursor()

# Drop and recreate the table
cursor.execute('DROP TABLE IF EXISTS foods')
cursor.execute('''
    CREATE TABLE foods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        food_name TEXT NOT NULL UNIQUE,
        chinese_name TEXT,
        category TEXT,
        description TEXT,
        is_gluten_free BOOLEAN NOT NULL
    )
''')

# Populate the table with data from the CSV
for _, row in data.iterrows():
    food_name = row['Food'].strip().lower()
    chinese_name = row['ChineseName'].strip().lower() if not pd.isna(row['ChineseName']) else None
    category = row['Category'].strip().lower() if not pd.isna(row['Category']) else None
    description = row['Description'] if not pd.isna(row['Description']) else None
    is_gluten_free = 0  # All items are not gluten-free as per your CSV

    cursor.execute('''
        INSERT OR IGNORE INTO foods (food_name, chinese_name, category, description, is_gluten_free)
        VALUES (?, ?, ?, ?, ?)
    ''', (food_name, chinese_name, category, description, is_gluten_free))

# Commit changes and close the connection
conn.commit()
conn.close()
print("Database populated successfully from CSV.")
