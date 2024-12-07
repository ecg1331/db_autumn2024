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
            SELECT Item, Price
            FROM Drinks
            WHERE Season = 'Fall';
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
        'query_7': '''
            SELECT B.Title
            FROM Books as B
            JOIN Skews AS S ON S.Skew = B.ISBN
            JOIN Sales_Item AS SI on SI.Item = S.Skew
            JOIN Sales AS SAL on SAL.Sale_ID = SI.Sale_ID
            WHERE B. Genre = 'Fantasy' AND YEAR(SAL.Sale_Date) = %s;
        '''
        # Add more queries as needed
    }

    # Check if the query_type exists in the dictionary
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

