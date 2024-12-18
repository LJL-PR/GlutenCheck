from flask import Flask, render_template, request, redirect, url_for
from fuzzywuzzy import fuzz
import sqlite3

app = Flask(__name__)

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('db/food_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Homepage route
@app.route('/')
def index():
    conn = get_db_connection()
    categories = conn.execute('''
        SELECT DISTINCT TRIM(LOWER(category)) AS category 
        FROM foods 
        WHERE category IS NOT NULL
    ''').fetchall()
    conn.close()
    return render_template('index.html', categories=categories)

# Search route
@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query').strip().lower()
    conn = get_db_connection()
    foods = conn.execute('SELECT * FROM foods').fetchall()
    conn.close()

    # Use fuzzy matching to find close matches
    results = []
    for food in foods:
        food_name = food['food_name'].lower()
        chinese_name = food['chinese_name'].lower() if food['chinese_name'] else ''
        category = food['category'].lower() if food['category'] else ''

        # Compare query against name, Chinese name, and category
        if (fuzz.partial_ratio(query, food_name) > 80 or
            fuzz.partial_ratio(query, chinese_name) > 80 or
            fuzz.partial_ratio(query, category) > 80):
            results.append(food)

    gluten_free = not bool(results)  # If no results, consider it gluten-free
    return render_template('search_results.html', results=results, query=query, gluten_free=gluten_free)

if __name__ == '__main__':
    app.run(debug=True)
