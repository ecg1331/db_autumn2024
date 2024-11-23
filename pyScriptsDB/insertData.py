import pandas as pd
import mysql.connector
from datetime import datetime
import os

# establishing connection
conn = mysql.connector.connect(user = 'root',
                               password = ' ',
                               host = 'localhost',
                               database = 'MyCoffeeShop'
                               )
print(conn)
curr = conn.cursor()


direct = os.path.dirname(os.path.abspath(__file__))

# INSERTING DATA
# Menu
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


# Ingredients
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

# recipes
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


# books
try:
    books_insert = """
    INSERT INTO Books
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    file_path = os.path.join(direct, "tables/books.csv")
    books = pd.read_csv(file_path, index_col=False)
    books['publication_date'] = books['publication_date'].apply(lambda x: datetime.strptime(x, "%m/%d/%Y").strftime("%Y-%m-%d"))
    booksLst = [tuple(row) for row in books.values.tolist()]
    curr.executemany(books_insert, booksLst)
    conn.commit()

except Exception as e:
    print(f"Errror inserting books data: {e}")


# drinks
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


# pastries
try:
    pastries_insert = """
    INSERT INTO Pastries
    VALUES (%s, %s, %s, %s)
    """
    file_path = os.path.join(direct, "tables/pastries_table.csv")
    print(file_path)
    pastries = pd.read_csv(file_path, index_col=False)
    pastriesList = [tuple(row) for row in pastries.values.tolist()]
    print(pastriesList)
    curr.executemany(pastries_insert, pastriesList)
    conn.commit()

except Exception as e:
    print(f"Error inserting pastry data: {e}")


print("Completed")
curr.close()
conn.close()