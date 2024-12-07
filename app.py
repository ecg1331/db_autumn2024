from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        user='root',
        password='Mori1331!',
        host='localhost',
        database='MyCoffeeShop'
    )


# Function to execute SQL queries
def execute_query(query):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.commit()  # Commit changes if necessary (useful for insert/update)
    cursor.close()
    connection.close()
    return result

# Route to handle different queries based on the button clicked (GET request)
@app.route('/run_query/<query_type>', methods=['GET'])
def run_query_get(query_type):
    # Define your queries here
    queries = {
        'query_1': "SELECT * FROM table1;",
        'query_2': '''
            SELECT ItemName
            FROM Menu
            WHERE Category = 'Breakfast';
        ''',
        'query_3': "SELECT * FROM table3;",
        # Add more queries as needed
    }

    # Check if the query_type exists in the dictionary
    if query_type in queries:
        result = execute_query(queries[query_type])
        return jsonify(result)  # Send back query result as JSON
    else:
        return jsonify({"error": "Invalid query type"}), 400

# Main route (home page)
@app.route('/')
def home():
    return render_template('index.html')

# Features page route
@app.route('/features')
def features():
    return render_template('features.html')

# POST route to handle form submissions for custom queries
@app.route('/run_query', methods=['POST'])
def run_query_post():
    query = request.form['query']
    
    # Connect to the database and execute the query
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]  # Get column names
        
        # Commit any changes (if query was an update/insert)
        conn.commit()
    except Exception as e:
        result = str(e)  # Show error message if query fails
        columns = []
    finally:
        cursor.close()
        conn.close()
    
    # Return the result to the template
    return render_template('index.html', result=result, columns=columns, query=query)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
