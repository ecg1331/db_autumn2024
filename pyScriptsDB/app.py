from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, request, redirect, url_for

import mysql.connector
import re

app = Flask(__name__)

# MySQL Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='MyCoffeeShop'
    )


def execute_query(query, params=None):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Execute the query with parameters (if any)
        cursor.execute(query, params or ())
        
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


# def execute_query(query):
#     connection = None
#     cursor = None
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute(query)
#         result = cursor.fetchall()
        
#         # Get column names from the cursor description
#         columns = [column[0] for column in cursor.description]
#         print(f"Columns: {columns}")  # Debugging: Print column names

#         # Convert each row to a dictionary, with column names as keys
#         result_dict = []
#         for row in result:
#             row_dict = {}
#             for i, column in enumerate(columns):
#                 row_dict[column] = row[i]  # Map column name to value
#             result_dict.append(row_dict)

#         print(f"Result: {result_dict}")  # Debugging: Print result after mapping
#         return result_dict  # Return a list of dictionaries

#     except mysql.connector.Error as err:
#         return {"error": f"Database error: {err}"}
#     except Exception as e:
#         return {"error": f"An unexpected error occurred: {e}"}
#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()


#     # connection.commit()  # Commit changes if necessary
#     # cursor.close()
#     # connection.close()

#     # # Flatten the result if it only contains one column
#     # if result and len(result[0]) == 1:
#     #     return [row[0] for row in result]
#     # return result

# Route to handle different queries based on the button clicked (GET request)
@app.route('/run_query/<query_type>', methods=['GET'])
def run_query_get(query_type):
    # Define your queries here
    queries = {
        'query_1': """
            SELECT D.Item AS Beverage, P.PastryName AS Pastry, (D.Price + P.Price - Pair.Discount) AS Price
            FROM Drinks AS D
            JOIN Pairs AS Pair ON D.DrinkSkew = Pair.DrinkSkew
            JOIN Pastries AS P ON Pair.PastrySkew = P.PastrySkew
            WHERE D.Season = %s
            ORDER BY Price DESC;
            """,
        'query_2': '''
            SELECT 
                M.ItemName AS ITEM,
                SUM(SI.Quantity) AS AMTSOLD
            FROM 
                Sales_Item AS SI
            JOIN 
                Menu AS M ON SI.Item = M.MenuItemSkew
            WHERE 
                M.Category = 'Breakfast'
            GROUP BY 
                M.ItemName
            ORDER BY 
                AMTSOLD DESC
            ;
        ''',
        'query_3': """
            SELECT 
                (SELECT 
                    SUM(SKEW.Price * SI.Quantity)
                FROM
                    Sales_Item AS SI
                JOIN  
                    Skews AS SKEW ON SI.Item = SKEW.Skew
                JOIN 
                    Sales AS SALES ON SALES.Sale_ID = SI.Sale_ID
                WHERE
                    YEAR(SALES.Sale_Date) = 2023) 
                -
                (SELECT 
                    SUM(SKEW.Price * SI.Quantity)
                FROM
                    Sales_Item AS SI
                JOIN  
                    Skews AS SKEW ON SI.Item = SKEW.Skew
                JOIN 
                    Sales AS SALES ON SALES.Sale_ID = SI.Sale_ID
                WHERE
                    YEAR(SALES.Sale_Date) = 2022) AS SalesDifference;
        """,
        'query_4': """
            SELECT B.Name AS Name, SUM(SKU.Price * SI.Quantity) AS TotalSales
                FROM Skews AS SKU
                JOIN Sales_Item AS SI ON SI.Item = SKU.Skew
                JOIN Sales AS S on S.Sale_ID = SI.Sale_ID
                JOIN Baristas AS B ON B.Employee_ID = S.Employee_ID 
                GROUP BY B.Employee_ID
                ORDER BY TotalSales DESC;
        """,
        'query_5': """
            SELECT 
                B.Genre, COUNT(SI.Item) as COUNT
            FROM
                Books as B
            JOIN 
                Sales_Item AS SI ON SI.Item = B.ISBN
            GROUP BY 
                B.Genre
            ORDER BY 
                COUNT DESC;
        """,
        'query_6': """
        SELECT B.Name AS Name, B.Phone AS PhoneNumber, COUNT(SI.Quantity) AS CakeSold
        FROM Pastries AS P
        JOIN Sales_Item AS SI ON SI.Item = P.PastrySkew 
        JOIN Sales AS S on S.Sale_ID = SI.Sale_ID
        JOIN Baristas AS B ON B.Employee_ID = S.Employee_ID
        WHERE P.PastryName = 'Vegan Carrot Cake'
        GROUP BY B.Name, B.Phone
        ORDER BY CakeSold DESC;
        """,
        'query_7': '''
            SELECT B.Title
            FROM Books as B
            JOIN Skews AS S ON S.Skew = B.ISBN
            JOIN Sales_Item AS SI on SI.Item = S.Skew
            JOIN Sales AS SAL on SAL.Sale_ID = SI.Sale_ID
            WHERE B. Genre = 'Fantasy' AND YEAR(SAL.Sale_Date) = %s;
        ''',
        'query_8': """
            SELECT I.IngredientName AS Ingredient, COUNT(R.IngredientSkew) AS NumberOfMenuItems, Max(M.Price) AS MaxPriceMenuItem
                FROM Recipes AS R
                JOIN Menu AS M ON R.MenuItemSkew = M.MenuItemSkew
                JOIN Ingredients AS I ON R.IngredientSkew = I.IngredientSkew
                GROUP BY I.IngredientName
                HAVING COUNT(R.IngredientSkew) > 3
                ORDER BY COUNT(R.IngredientSkew) DESC;
        """,
        'query_9': """
        SELECT 
            CL.Name, CL.Loyalty_ID, COUNT(S.Sale_ID) AS Visits
        FROM 
            Customer_Loyalty as CL
        JOIN
            Sales AS S ON S.Customer_Loyalty_ID = CL.Loyalty_ID
        GROUP BY
            CL.Loyalty_ID
        HAVING 
            Visits > 3
        ORDER BY
            Visits DESC;
        """,
        'query_10': """
        SELECT M.Category, COUNT(M.MenuItemSkew) AS MenuItemCount, SUM(SI.Quantity) As QuantitySold, SUM(M.Price * SI.Quantity) AS TotalSales
            FROM Menu AS M
            JOIN Sales_Item AS SI ON SI.Item = M.MenuItemSkew
            GROUP BY M.Category
            ORDER BY M.Category;
        """
        # Add more queries as needed
    }
    if query_type == 'query_1':
        season = request.args.get('season', default="Year-Round", type=str)  # Get season from the query parameter
        query = queries[query_type]
        result = execute_query(query, (season,))
        return jsonify(result)
    elif query_type == 'query_7':
        year = request.args.get('year', default=2024, type=int)  # Get year from the query parameter
        # Validate the year
        if 2018 <= year <= 2024:
            query = queries[query_type]
            result = execute_query(query, (year,))
            return jsonify(result)
        else:
            return jsonify({"error": "Sorry! You must enter a four-digit integer between 2018 and 2024. Otherwise, we will use the default year of 2024."}), 400
    elif query_type in queries:
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

queries = {
    'query_baristas': "SELECT * FROM Baristas LIMIT 10",
    'query_sales': "SELECT * FROM Sales LIMIT 10",
    'query_skews': "SELECT * FROM Skews LIMIT 10",
    'query_books': "SELECT * FROM Books LIMIT 10",
    'query_customer_loyalty': "SELECT * FROM Customer_Loyalty LIMIT 10",
    'query_drinks': "SELECT * FROM Drinks LIMIT 10",
    'query_ingredients': "SELECT * FROM Ingredients LIMIT 10",
    'query_menu': "SELECT * FROM Menu LIMIT 10",
    'query_pairs': "SELECT * FROM Pairs LIMIT 10",
    'query_pastries': "SELECT * FROM Pastries LIMIT 10",
    'query_recipes': "SELECT * FROM Recipes LIMIT 10",
    'query_sales_items': "SELECT * FROM Sales_Item LIMIT 10"
}


# Features page route
@app.route('/tables', methods=['GET', 'POST'])
def tables():
    table_data = {}
    table_columns = {}

    # Handle form submission
    if request.method == 'POST':
        # Get the table name and data from the form
        table_name = request.form.get('table_name')
        form_data = {key: request.form[key] for key in request.form if key != 'table_name'}

        # Dynamically generate the INSERT query based on the table and form data
        columns = get_table_columns(table_name)
        placeholders = ', '.join(['%s'] * len(form_data))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        params = tuple(form_data[column] for column in columns)
        table_data = get_tables()  # This should return a list of table names, not a Response object
        # Ensure that the function returns a list
        if not isinstance(table_data, list):
            raise TypeError("Expected a list of table names, but got something else.")
        
        # Get columns for each table
        table_columns = {table_name: get_table_columns(table_name) for table_name in table_data}
        
        # Execute the insert query
        result = execute_query(query, params)

        # Optionally, refresh table data after insertion
        table_data = fetch_table_data()

    else:
        # Fetch table data and columns if no form submission
        table_data = fetch_table_data()

    return render_template('tables.html', table_data=table_data, table_columns=table_columns)

def fetch_table_data():
    # Fetch data for all tables
    table_data = {}
    table_queries = {
        'Baristas': 'query_baristas',
        'Sales': 'query_sales',
        'Skews': 'query_skews',
        'Ingredients': 'query_ingredients',
        'Books': 'query_books',
        'Customer_Loyalty': 'query_customer_loyalty',
        'Menu': 'query_menu',
        'Pairs': 'query_pairs',
        'Recipes': 'query_recipes',
        'Drinks': 'query_drinks',
        'Sales_Item': 'query_sales_items',
        'Pastries': 'query_pastries'
    }

    for table_name, query_key in table_queries.items():
        if query_key in queries:
            result = execute_query(queries[query_key])
            table_data[table_name] = result
    return table_data

def get_table_columns(table_name):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = cursor.fetchall()

    connection.close()

    # Extract column names
    column_names = [column[0] for column in columns]  # column[0] is the column name

    return column_names
def get_table_data(table_name):
    try:
        # Establish the database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Define the query to fetch all data from the specified table
        query = f"SELECT * FROM {table_name}"

        # Execute the query
        cursor.execute(query)
        result = cursor.fetchall()

        # Get the column names from the cursor description
        columns = [column[0] for column in cursor.description]

        # Convert the rows into a list of dictionaries
        result_dict = []
        for row in result:
            row_dict = {}
            for i, column in enumerate(columns):
                row_dict[column] = row[i]  # Map column name to its value in the row
            result_dict.append(row_dict)

        return result_dict  # Return the list of dictionaries

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/add_entry/<table_name>', methods=['GET', 'POST'])
def add_entry(table_name):
    if request.method == 'POST':
        # Get the form data (all fields sent in the POST request)
        form_data = request.form.to_dict()
        
        # Remove table_name from form data (since it's already in the URL)
        form_data.pop('table_name', None)
        
        # Build the query to insert data into the table
        columns = ', '.join(form_data.keys())
        values = ', '.join([f"'{v}'" for v in form_data.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        
        # Execute the query (you need to define your execute_query function)
        execute_query(query)

        # Redirect to the tables page (or another page if needed)
        return redirect(url_for('tables'))
    
    # If it's a GET request (this part is for showing the form initially), render a confirmation page
    return render_template('tables.html', table_data=table_data, table_columns=table_columns)

@app.route('/get_table_columns/<table_name>', methods=['GET'])
def get_columns(table_name):
    columns = get_table_columns(table_name)
    return jsonify(columns)

@app.route('/view_table/<table_name>', methods=['GET'])
def view_table(table_name):
    # Fetch the table columns and data from your database or query
    table_columns = get_table_columns(table_name)
    table_data = get_table_data(table_name)
    
    return render_template('tables.html', 
                           table_name=table_name, 
                           table_columns=table_columns, 
                           table_data=table_data)

@app.route('/get_tables', methods=['GET'])
def get_tables():
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # Query to get the table names
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()  # This will return a list of tuples

        # Extract table names from the tuples
        table_names = [table[0] for table in tables]

        return jsonify(table_names)  # Return table names as JSON
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/run_query', methods=['GET'])
def run_table_query():
    table_name = request.args.get('table_name')
    
    query_mapping = {
        'Baristas': 'query_baristas',
        'Sales': 'query_sales',
        'Skews': 'query_skews',
        'Ingredients': 'query_ingredients',
        'Books': 'query_books',
        'Customer_Loyalty': 'query_customer_loyalty',
        'Menu': 'query_menu',
        'Pairs': 'query_pairs',
        'Recipes': 'query_recipes',
        'Drinks': 'query_drinks',
        'Sales_Item': 'query_sales_items',
        'Pastries': 'query_pastries'  # Add Pastries query mapping here

    }

    if table_name in query_mapping:
        query_key = query_mapping[table_name]
        result = execute_query(queries[query_key])
        table_columns = get_table_columns(table_name)
        return render_template('tables.html', table_data={table_name: result})
    else:
        return jsonify({"error": f"Query for table '{table_name}' not defined."}), 400

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

