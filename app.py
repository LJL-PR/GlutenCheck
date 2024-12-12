from flask import Flask, render_template, request
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

    # Search in both name and category
    results = conn.execute(
        '''
        SELECT * FROM foods 
        WHERE lower(food_name) = ? 
        OR lower(chinese_name) = ? 
        OR lower(category) = ?
        ''',
        (query, query, query)
    ).fetchall()

    conn.close()

    gluten_free = not bool(results)  # If no results, consider gluten-free
    return render_template('search_results.html', results=results, query=query, gluten_free=gluten_free)

if __name__ == '__main__':
    app.run(debug=True)
