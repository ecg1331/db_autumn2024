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

#1. Menu
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

#2. Ingredients
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


#3. Recipies
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


#4. Books
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


#5. Drinks
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


#6. Pastries
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

#7. Baristas
try:
    barista_table = """
    CREATE TABLE Baristas (
    Employee_ID      INT     NOT NULL,
    Name             VARCHAR(20),
    Phone            VARCHAR(15),
    PRIMARY KEY (Employee_ID)
    );
    """
    curr.execute(barista_table)
except Exception as e:
    print(f"Error creating baristas table: {e}")


# 8. Customer Loyalty
try:
    customer_table = """
    CREATE TABLE Customer_Loyalty (
    Loyalty_ID       INT     NOT NULL,
    Name             VARCHAR(25),
    Birthday         DATE,
    Email            VARCHAR(40),
    PRIMARY KEY (Loyalty_ID)
    );
    """
    curr.execute(customer_table)
except Exception as e:
    print(f"Error creating CL table: {e}")


# 9. Sales
try:
    sales_table = """
            CREATE TABLE Sales (
            Sale_ID            INT     NOT NULL,
            Employee_ID         INT,
            Customer_Loyalty_ID INT,
            Sale_Date           DATE,
            PRIMARY KEY (Sale_ID),
            FOREIGN KEY (Employee_ID) REFERENCES Baristas(Employee_ID),
            FOREIGN KEY (Customer_Loyalty_ID) REFERENCES Customer_Loyalty(Loyalty_ID)
            );
            """
    curr.execute(sales_table)
except Exception as e:
    print(f"Error creating sales table: {e}")


# 10. Skews Table
try:
    skew_table = """
            CREATE TABLE Skews(
            Skew     VARCHAR(10)      NOT NULL,
            PRIMARY KEY (Skew)
            );
            """
    curr.execute(skew_table)
except Exception as e:
    print(f"Error creating skew table: {e}")


# 11. Sales Item
try:
    sales_item = """
            CREATE TABLE Sales_Item(
            Sale_ID     INT      NOT NULL,
            Item        VARCHAR(11),
            Quantity    INT,
            PRIMARY KEY (Sale_ID, Item),
            FOREIGN KEY (Sale_ID) REFERENCES Sales(Sale_ID),
            FOREIGN KEY (Item) REFERENCES Skews(Skew)
            );
            """
    curr.execute(sales_item)
except Exception as e:
    print(f"Error creating sales item table: {e}")


    
curr.execute("SHOW TABLES;")
print("Tables: ", curr.fetchall())


curr.close()
conn.close()

