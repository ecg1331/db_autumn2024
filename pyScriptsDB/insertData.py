import pandas as pd
import mysql.connector
from datetime import datetime
import os

# establishing connection
conn = mysql.connector.connect(user = 'root',
                               password = 'Salt%eeny7',
                               host = 'localhost',
                               database = 'MyCoffeeShop'
                               )
print(conn)
curr = conn.cursor()


direct = os.path.dirname(os.path.abspath(__file__))
# INSERTING DATA

# 1. Skew
try:
    skew_query = """
    INSERT INTO Skews
    VALUES (%s, %s)
    """
    file_path = os.path.join(direct, "tables/skews_table.csv")
    skew = pd.read_csv(file_path, index_col=False)
    skewList = [tuple(row) for row in skew.values.tolist()]
    curr.executemany(skew_query, skewList)
    conn.commit()
except Exception as e:
    print(f"Error inserting into skew table: {e}")


# 2. Menu
try:
    file_path = os.path.join(direct, "tables/menu_items_table.csv")
    menu_csv = pd.read_csv(file_path, index_col=False)
    menuList = [tuple(row) for row in menu_csv.values.tolist()]
    menu_insert = """
            INSERT INTO Menu
            VALUES (%s, %s, %s, %s)
            """
    curr.executemany(menu_insert, menuList)
    conn.commit()

except Exception as e:
    print(f"Error inserting menu data: {e}")


# 3. Ingredients
try:
    file_path = os.path.join(direct, "tables/ingredients_table.csv")
    ingredients = pd.read_csv(file_path, index_col=False)
    ingredients_lst = [tuple(row) for row in ingredients.values.tolist()]
    ingredients_insert = """
                INSERT INTO Ingredients
                VALUES (%s, %s)
                """
    curr.executemany(ingredients_insert, ingredients_lst)
    conn.commit()

except Exception as e:
    print(f"Error inserting ingredient data: {e}")

# 4. Receipes
try:
    file_path = os.path.join(direct, "tables/recipes_table.csv")
    recipes = pd.read_csv(file_path, index_col=False)
    recipes_lst = [tuple(row) for row in recipes.values.tolist()]
    recipes_insert = """
                INSERT INTO Recipes
                VALUES (%s, %s)
                """
    curr.executemany(recipes_insert, recipes_lst)
    conn.commit()

except Exception as e:
    print(f"Errror inserting recipes data: {e}")


# 5. Books
try:
    books_insert = """
    INSERT INTO Books
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    file_path = os.path.join(direct, "tables/books.csv")
    books = pd.read_csv(file_path, index_col=False)
    books['publication_date'] = books['publication_date'].apply(lambda x: datetime.strptime(x, "%m/%d/%Y").strftime("%Y-%m-%d"))
    booksLst = [tuple(row) for row in books.values.tolist()]
    curr.executemany(books_insert, booksLst)
    conn.commit()

except Exception as e:
    print(f"Errror inserting books data: {e}")


# 6. Drinks
try:
    drink_insert = """
    INSERT INTO Drinks
    VALUES (%s, %s, %s, %s, %s)
    """
    file_path = os.path.join(direct, "tables/drink_table.csv")
    drinks = pd.read_csv(file_path, index_col=False)
    drinkLst = [tuple(row) for row in drinks.values.tolist()]
    curr.executemany(drink_insert, drinkLst)
    conn.commit()

except Exception as e:
    print(f"Error inserting drinks data: {e}")


# 7. Pastries
try:
    pastries_insert = """
    INSERT INTO Pastries
    VALUES (%s, %s, %s, %s)
    """
    file_path = os.path.join(direct, "tables/pastries_table.csv")
    pastries = pd.read_csv(file_path, index_col=False)
    pastriesList = [tuple(row) for row in pastries.values.tolist()]
    curr.executemany(pastries_insert, pastriesList)
    conn.commit()
except Exception as e:
    print(f"Error inserting pastry data: {e}")


# 8. Baristas
try:
    barista_insert = """
    INSERT INTO Baristas
    VALUES (%s, %s, %s)
    """
    file_path = os.path.join(direct, "tables/barista_table.csv")
    barista = pd.read_csv(file_path, index_col=False)
    baristaList = [tuple(row) for row in barista.values.tolist()]
    curr.executemany(barista_insert, baristaList)
    conn.commit()
except Exception as e:
    print(f"Error inserting into barista table: {e}")


# 9. Customer Loyalty
try:
    cl_query = """
    INSERT INTO Customer_Loyalty
    VALUES (%s, %s, %s, %s)
    """
    file_path = os.path.join(direct, "tables/CL_table.csv")
    cl = pd.read_csv(file_path, index_col=False)
    clList = [tuple(row) for row in cl.values.tolist()]
    curr.executemany(cl_query, clList)
    conn.commit()
except Exception as e:
    print(f"Error inserting into cl table: {e}")


# 10. Sales
try:
    sales_query = """
    INSERT INTO Sales
    VALUES (%s, %s, %s, %s)
    """
    file_path = os.path.join(direct, "tables/sales_table.csv")
    sales = pd.read_csv(file_path, index_col=False)
    salesList = [tuple(row) for row in sales.values.tolist()]
    curr.executemany(sales_query, salesList)
    conn.commit()
except Exception as e:
    print(f"Error inserting into sales table: {e}")


# 11. Sales Item
try:
    sales_item_query = """
    INSERT INTO Sales_Item
    VALUES (%s, %s, %s)
    """
    file_path = os.path.join(direct, "tables/sales_item_table.csv")
    sales_item = pd.read_csv(file_path, index_col=False)
    siList = [tuple(row) for row in sales_item.values.tolist()]
    curr.executemany(sales_item_query, siList)
    conn.commit()
except Exception as e:
    print(f"Error inserting into sales item table: {e}")

# 12. Pairs Item
try:
    pairs_query = """
    INSERT INTO Pairs
    VALUES (%s, %s, %s, %s)
    """
    file_path = os.path.join(direct, "tables/pairs_table.csv")
    pairs_item = pd.read_csv(file_path, index_col=False)
    pairsList = [tuple(row) for row in pairs_item.values.tolist()]
    curr.executemany(pairs_query, pairsList)
    conn.commit()
except Exception as e:
    print(f"Error inserting into sales item table: {e}")


print("Completed")
curr.close()
conn.close()