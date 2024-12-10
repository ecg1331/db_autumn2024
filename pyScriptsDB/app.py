from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, request, redirect, url_for

import logging

logging.basicConfig(level=logging.DEBUG)  # Ensure debug-level logging

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

        cursor.execute(query, params or ())

        # Ensure all results are read
        result = cursor.fetchall()  # Fetch all results

        # Get column names
        columns = [column[0] for column in cursor.description]

        # Convert the result into a dictionary
        result_dict = []
        for row in result:
            row_dict = {columns[i]: row[i] for i in range(len(columns))}
            result_dict.append(row_dict)

        return result_dict

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}
    except Excption as e:
        return {"error": f"An unexpected error occurred: {e}"}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Route to handle different queries based on the button clicked (GET request)
@app.route('/run_query/<query_type>', methods=['GET'])
def run_query_get(query_type):
    # Define your queries here
    queries = {
        'query_1': """
            SELECT D.Item AS Beverage, P.PastryName AS Pastry, (D.Price + P.Price - Pair.Discount) AS Price
            FROM Drinks AS D
            JOIN Pairs AS Pair ON D.DrinkSKU = Pair.DrinkSKU
            JOIN Pastries AS P ON Pair.PastrySKU = P.PastrySKU
            WHERE D.Season = 'Fall'
            ORDER BY Price DESC;
            """,
        'query_2': '''
            SELECT 
                M.ItemName AS ITEM,
                SUM(SI.Quantity) AS AMTSOLD
            FROM 
                Sales_Item AS SI
            JOIN 
                Menu AS M ON SI.Item = M.MenuItemSKU
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
                    SUM(SKU.Price * SI.Quantity)
                FROM
                    Sales_Item AS SI
                JOIN  
                    SKUs AS SKU ON SI.Item = SKU.SKU
                JOIN 
                    Sales AS SALES ON SALES.Sale_ID = SI.Sale_ID
                WHERE
                    YEAR(SALES.Sale_Date) = 2023) 
                -
                (SELECT 
                    SUM(SKU.Price * SI.Quantity)
                FROM
                    Sales_Item AS SI
                JOIN  
                    SKUs AS SKU ON SI.Item = SKU.SKU
                JOIN 
                    Sales AS SALES ON SALES.Sale_ID = SI.Sale_ID
                WHERE
                    YEAR(SALES.Sale_Date) = 2022) AS SalesDifference;
        """,
        'query_4': """
            SELECT B.Name AS Name, SUM(SKU.Price * SI.Quantity) AS TotalSales
                FROM SKUs AS SKU
                JOIN Sales_Item AS SI ON SI.Item = SKU.SKU
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
        JOIN Sales_Item AS SI ON SI.Item = P.PastrySKU 
        JOIN Sales AS S on S.Sale_ID = SI.Sale_ID
        JOIN Baristas AS B ON B.Employee_ID = S.Employee_ID
        WHERE P.PastryName = 'Vegan Carrot Cake'
        GROUP BY B.Name, B.Phone
        ORDER BY CakeSold DESC;
        """,
        'query_7': '''
            SELECT B.Title
            FROM Books as B
            JOIN SKUs AS S ON S.SKU = B.ISBN
            JOIN Sales_Item AS SI on SI.Item = S.SKU
            JOIN Sales AS SAL on SAL.Sale_ID = SI.Sale_ID
            WHERE B. Genre = 'Fantasy' AND YEAR(SAL.Sale_Date) = %s;
        ''',
        'query_8': """
            SELECT I.IngredientName AS Ingredient, COUNT(R.IngredientSKU) AS NumberOfMenuItems, Max(M.Price) AS MaxPriceMenuItem
                FROM Recipes AS R
                JOIN Menu AS M ON R.MenuItemSKU = M.MenuItemSKU
                JOIN Ingredients AS I ON R.IngredientSKU = I.IngredientSKU
                GROUP BY I.IngredientName
                HAVING COUNT(R.IngredientSKU) > 3
                ORDER BY COUNT(R.IngredientSKU) DESC;
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
        SELECT M.Category, COUNT(M.MenuItemSKU) AS MenuItemCount, SUM(SI.Quantity) As QuantitySold, SUM(M.Price * SI.Quantity) AS TotalSales
            FROM Menu AS M
            JOIN Sales_Item AS SI ON SI.Item = M.MenuItemSKU
            GROUP BY M.Category
            ORDER BY M.Category;
        """
    }
    if query_type == 'query_7':
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

@app.route('/about')
def about():
    return render_template('about.html')

# Features page route
@app.route('/features')
def features():
    return render_template('features.html')

queries = {
    'query_baristas': "SELECT * FROM Baristas",
    'query_sales': "SELECT * FROM Sales LIMIT 10",
    'query_skus': "SELECT * FROM SKUs LIMIT 10",
    'query_books': "SELECT * FROM Books LIMIT 10",
    'query_customer_loyalty': "SELECT * FROM Customer_Loyalty",
    'query_drinks': "SELECT * FROM Drinks",
    'query_ingredients': "SELECT * FROM Ingredients",
    'query_menu': "SELECT * FROM Menu",
    'query_pairs': "SELECT * FROM Pairs LIMIT 10",
    'query_pastries': "SELECT * FROM Pastries",
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
        'SKUs': 'query_skus',
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

@app.route('/add_data')
def add_data():
    # Pass the table data to the template
    table_data = get_all_tables()  
    return render_template('add_data.html', table_data=table_data)

def get_all_tables():
    return {
        'Baristas': {'image_url': 'static/cat_wash.jpg'},
        'Ingredients': {'image_url': 'static/cat_plant.jpg'},
        'Customer_Loyalty': {'image_url': 'static/cat_knit.jpg'},
        'Menu': {'image_url': 'static/cat_table.jpg'},
        'Drinks': {'image_url': 'static/cat_sleep.jpg'},
        'Pastries': {'image_url': 'static/cat_cake.jpg'}
        }
        # Add other tables and images here
    
@app.route('/add_entry/<table_name>', methods=['GET', 'POST'])
def add_entry(table_name):
    print(f"Attempting to add data to table: {table_name}") 

    validation_rules = {
        "Menu": {
            "MenuItemSKU": ['number', "sku_number"],
            "Category": ["dropdown", ["Breakfast", "Salads, Sandwiches & Baguettes", "Tartines & Plein Bowls"]],
            "Price": ["number", "integer_or_decimal"],
            "ItemName": ["text", "alpha_plus"]
        },
        "Drinks": {
            "DrinkSKU": ['number', "sku_number"],
            "Item": ["text", "alpha_plus"],
            "Price": ["number", "integer_or_decimal"],
            "Category": ["dropdown", ["Espresso Bar", "Brew Bar", "Specialty Bar", "Seasonal Drinks"]],
            "Season": ["dropdown", ["Year-Round", "Fall", "Spring", "Winter", "Summer"]],
        },
        "Baristas": {
            "Employee_ID": ['number', "number"],  # Ensure this field exists for Barista
            'Name': ["text", 'name_format'],
            'Phone': ["number", "phone"]
        },
        "Ingredients": {
            "IngredientSKU" : ['number', "sku_number"],
            "IngredientName": ['text', 'alpha']
        },
        "Customer_Loyalty": {
            "Loyalty_ID": ['number', "number"],
            'Name': ["text", 'name_format'],
            "Email": ["text", "email"],
            "Birthday": ["date", "date"]
        },
        "Pastries": {
            "PastrySKU": ['number', "sku_number"],
            "PastryName": ["text", "alpha_plus"],
            "Price": ["number", "integer_or_decimal"],
            "Sell_By_Date": ["date", "date"]                
        }
    }

    # Retrieve the validation rules for the current table.
    table_validation_rules = validation_rules.get(table_name, {})
    
    print(f"Validation rules for {table_name}: {table_validation_rules}") 

    # Get the columns for the table dynamically
    table_columns = get_table_columns(table_name)
    table_data = get_all_tables()  

    if request.method == 'POST':
        form_data = request.form.to_dict()
        print("Form Data:", form_data)  

        # Remove 'table_name' if it exists in form_data
        form_data.pop('table_name', None)

        # Get the primary key column dynamically for the table
        primary_key_column = get_primary_key_column(table_name)
        
        if primary_key_column:
            primary_key_value = form_data.get(primary_key_column)
            print(f"Checking for duplicate {primary_key_column}: {primary_key_value}")  

            if primary_key_value:
                # Check if the primary key value already exists in the table
                existing_entry = execute_query(f"SELECT * FROM {table_name} WHERE {primary_key_column} = %s", (primary_key_value,))
                print(f"Existing entry check result: {existing_entry}")  
                if existing_entry:
                    error_message = f"Error: {primary_key_column} = {primary_key_value} already exists in the {table_name} table. Please use a unique value."
                    print(f"Error Message: {error_message}")
                    return render_template('add_entry_form.html', 
                                           table_name=table_name, 
                                           table_columns=table_columns, 
                                           table_data=table_data,
                                           error_message=error_message,
                                           form_data=form_data,
                                           validation_rules=table_validation_rules)
        
        # Proceed with the insert if no duplicates
        columns = ', '.join(form_data.keys())
        placeholders = ', '.join(['%s'] * len(form_data))  
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Convert form data to a tuple of values
        values = tuple(form_data[column] for column in form_data)
        print(f"Executing query: {query} with values: {values}")  
        
        try:
            result = execute_insert_query(query, values)
            
            if isinstance(result, dict) and "error" in result:
                # Log the error if it occurs
                logging.error(f"Error inserting data into {table_name}: {result['error']}")
                error_message = result["error"]
                return render_template('add_entry_form.html', 
                                       table_name=table_name, 
                                       validation_rules=table_validation_rules,
                                       table_columns=table_columns, 
                                       table_data=table_data,
                                       error_message=error_message)
            
            # If insert is successful, redirect to the tables page
            return redirect(url_for('tables'))
        except Exception as e:
            logging.error(f"Error executing query for {table_name}: {str(e)}")
            error_message = f"An error occurred while inserting the data: {str(e)}"
            return render_template('add_entry_form.html', 
                                   table_name=table_name, 
                                   validation_rules=table_validation_rules,
                                   table_columns=table_columns, 
                                   table_data=table_data,
                                   error_message=error_message,
                                   form_data=form_data)
        except mysql.connector.Error as err:
            logging.error(f"Error inserting data into {table_name}: {err}")
            error_message = f"Error inserting data: {err}"
            return render_template('add_entry_form.html', 
                                   table_name=table_name, 
                                   validation_rules=table_validation_rules,
                                   table_columns=table_columns, 
                                   table_data=table_data,
                                   error_message=error_message,
                                   form_data=form_data)

    # Return the form for the user to fill out if no POST request
    return render_template('add_entry_form.html', 
                           table_name=table_name, 
                           validation_rules=table_validation_rules,
                           table_columns=table_columns, 
                           table_data=table_data)
     
def execute_insert_query(query, params=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()  # Ensure the transaction is committed
        return True
    except mysql.connector.Error as err:
        # Check for duplicate entry error (1062 is the error code for duplicate entry)
        if err.errno == 1062:
            logging.error(f"Duplicate entry found for {params[0]}")  # Log the duplicate entry error
            return {"error": f"Duplicate entry for {params[0]}."}
        else:
            return {"error": f"Database error: {err}"}
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {"error": f"Unexpected error: {e}"}
    finally:
        cursor.close()
        conn.close()

def get_primary_key_column(table_name):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'"
    cursor.execute(query)
    result = cursor.fetchall()
    
    # If primary key is found, return the column name (first column in the result)
    if result:
        print(result)
        primary_key_column = result[0][4]  
        return primary_key_column
    return None  # If no primary key is found


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
        tables = cursor.fetchall()  

        table_names = [table[0] for table in tables]

        return jsonify(table_names)  
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
        'SKUs': 'query_skus',
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
        
        conn.commit()
    except Exception as e:
        result = str(e)  
        columns = []
    finally:
        cursor.close()
        conn.close()
    
    # Return the result to the template
    return render_template('index.html', result=result, columns=columns, query=query)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

