from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        user='root',
        password='Salt%eeny7',
        host='localhost',
        database='MyCoffeeShop'
    )

def execute_query(query):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Get column names from the cursor description
        columns = [column[0] for column in cursor.description]
        print(f"Columns: {columns}")  # Debugging: Print column names

        # Convert each row to a dictionary, with column names as keys
        result_dict = []
        for row in result:
            row_dict = {}
            for i, column in enumerate(columns):
                row_dict[column] = row[i]  # Map column name to value
            result_dict.append(row_dict)

        print(f"Result: {result_dict}")  # Debugging: Print result after mapping
        return result_dict  # Return a list of dictionaries

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


    # connection.commit()  # Commit changes if necessary
    # cursor.close()
    # connection.close()

    # # Flatten the result if it only contains one column
    # if result and len(result[0]) == 1:
    #     return [row[0] for row in result]
    # return result

# Route to handle different queries based on the button clicked (GET request)
@app.route('/run_query/<query_type>', methods=['GET'])
def run_query_get(query_type):
    # Define your queries here
    queries = {
        'query_1': """
            SELECT Item, Price
            FROM Drinks
            WHERE Season = 'Fall';
            """,
        'query_2': '''
            SELECT ItemName
            FROM Menu
            WHERE Category = 'Breakfast';
        ''',
        'query_3': "SELECT * FROM table3;",
        'query_7': '''
            SELECT Title
            FROM Books
            WHERE Genre = 'Fantasy'
            LIMIT 10;
        '''
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

from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        user='root',
        password=' ',
        host='localhost',
        database='MyCoffeeShop'
    )

def execute_query(query):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Get column names from the cursor description
        columns = [column[0] for column in cursor.description]
        print(f"Columns: {columns}")  # Debugging: Print column names

        # Convert each row to a dictionary, with column names as keys
        result_dict = []
        for row in result:
            row_dict = {}
            for i, column in enumerate(columns):
                row_dict[column] = row[i]  # Map column name to value
            result_dict.append(row_dict)

        print(f"Result: {result_dict}")  # Debugging: Print result after mapping
        return result_dict  # Return a list of dictionaries

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


    # connection.commit()  # Commit changes if necessary
    # cursor.close()
    # connection.close()

    # # Flatten the result if it only contains one column
    # if result and len(result[0]) == 1:
    #     return [row[0] for row in result]
    # return result

# Route to handle different queries based on the button clicked (GET request)
@app.route('/run_query/<query_type>', methods=['GET'])
def run_query_get(query_type):
    # Define your queries here
    queries = {
        'query_1': """
            SELECT Item, Price
            FROM Drinks
            WHERE Season = 'Fall';
            """,
        'query_2': '''
            SELECT ItemName
            FROM Menu
            WHERE Category = 'Breakfast';
        ''',
        'query_3': "SELECT * FROM table3;",
        'query_7': '''
            SELECT Title
            FROM Books
            WHERE Genre = 'Fantasy'
            LIMIT 10;
        '''
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
