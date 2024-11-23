import pandas as pd
import mysql.connector
from datetime import datetime

# establishing connection
conn = mysql.connector.connect(user = 'root',
                               password = ' ',
                               host = 'localhost',
                               )
print(conn)
curr = conn.cursor()

# creating DB
try:
    curr.execute("CREATE DATABASE MyCoffeeShop;")
    print("Database created successfully")
except Exception as e:
    print(f"Error creating database: {e}")

# CREATING TABLES
# MENU
curr.execute("USE MyCoffeeShop;")
try:
    menu_query = """
        CREATE TABLE Menu (
            MenuItemSkew INT    NOT NULL,
            ItemName    VARCHAR(45),
            Category    VARCHAR(35),
            Price       DECIMAL(4, 2),
            PRIMARY KEY (MenuItemSkew)
            );
            """
    curr.execute(menu_query)
except Exception as e:
    print(f"Errror creating menu table: {e}")

# INGREDIENTS
try:
    ingredient_table = """
        CREATE TABLE Ingredients (
            IngredientSkew      INT    NOT NULL,
            IngredientName      VARCHAR(30),
            PRIMARY KEY (IngredientSkew)
            );
            """
    curr.execute(ingredient_table)
except Exception as e:
    print(f"Errror creating ingredient table: {e}")


# RECIPES
try:
    recipe_table = """
        CREATE TABLE Recipes (
            MenuItemSkew INT NOT NULL,
            IngredientSkew INT NOT NULL,
            PRIMARY KEY (MenuItemSkew, IngredientSkew),
            FOREIGN KEY (MenuItemSkew) REFERENCES Menu(MenuItemSkew)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            FOREIGN KEY (IngredientSkew) REFERENCES Ingredients(IngredientSkew)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        """
    curr.execute(recipe_table)
except Exception as e:
    print(f"Error recipe ingredient table: {e}")


# books
try:
    books_table = """
    CREATE TABLE Books (
        ISBN            VARCHAR(10)     NOT NULL,
        Title           TEXT,
        Author          VARCHAR(35),
        NumPages        INT,
        Publishing_Date DATE,
        Publisher       VARCHAR(75),
        Genre          VARCHAR(40),
        PRIMARY KEY (ISBN)
    );
    """
    curr.execute(books_table)
except Exception as e:
    print(f"Error creating books table: {e}")


# drinks
try:
    drinks_table = """
    CREATE TABLE Drinks(
    DrinkSkew   INT     NOT NULL,
    Item        VARCHAR(35),
    Price       DECIMAL(4, 2),
    Category    VARCHAR(20),
    Season      VARCHAR(20),
    PRIMARY KEY (DrinkSkew)
    );
    """
    curr.execute(drinks_table)
except Exception as e:
    print(f"Error creating drinks table: {e}")


# pastries:
try:
    pastries_table = """
    CREATE TABLE Pastries (
    PastrySkew      INT     NOT NULL,
    PastryName      VARCHAR(40),
    Price           DECIMAL(4, 2),
    Sell_By_Date    DATE,
    PRIMARY KEY (PastrySkew)
    );
    """
    curr.execute(pastries_table)
except Exception as e:
    print(f"Error creating pastries table: {e}")

curr.execute("SHOW TABLES;")
print("Tables: ", curr.fetchall())


curr.close()
conn.close()

