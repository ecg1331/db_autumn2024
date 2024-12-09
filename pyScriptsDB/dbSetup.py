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
curr.execute("USE MyCoffeeShop;")

# 1. SKUs Table
try:
    sku_table = """
            CREATE TABLE SKUs(
            SKU     VARCHAR(10)      NOT NULL,
            Price     DECIMAL(4, 2),    
            PRIMARY KEY (SKU)
            );
            """
    curr.execute(sku_table)
except Exception as e:
    print(f"Error creating SKU table: {e}")

#2. Menu
try:
    menu_query = """
        CREATE TABLE Menu (
            MenuItemSKU VARCHAR(4)    NOT NULL,
            ItemName    VARCHAR(45),
            Category    VARCHAR(35),
            Price       DECIMAL(4, 2),
            PRIMARY KEY (MenuItemSKU),
            FOREIGN KEY (MenuItemSKU) REFERENCES SKUs(SKU)
            );
            """
    curr.execute(menu_query)
except Exception as e:
    print(f"Errror creating menu table: {e}")

#3. Ingredients
try:
    ingredient_table = """
        CREATE TABLE Ingredients (
            IngredientSKU      VARCHAR(4)    NOT NULL,
            IngredientName      VARCHAR(30),
            PRIMARY KEY (IngredientSKU)
            );
            """
    curr.execute(ingredient_table)
except Exception as e:
    print(f"Errror creating ingredient table: {e}")


#4. Recipies
try:
    recipe_table = """
        CREATE TABLE Recipes (
            MenuItemSKU VARCHAR(4) NOT NULL,
            IngredientSKU VARCHAR(4) NOT NULL,
            PRIMARY KEY (MenuItemSKU, IngredientSKU),
            FOREIGN KEY (MenuItemSKU) REFERENCES Menu(MenuItemSKU)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            FOREIGN KEY (IngredientSKU) REFERENCES Ingredients(IngredientSKU)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        """
    curr.execute(recipe_table)
except Exception as e:
    print(f"Error recipe ingredient table: {e}")


#5. Books
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
        Price           DECIMAL(4, 2),
        PRIMARY KEY (ISBN),
        FOREIGN KEY (ISBN) REFERENCES SKUs(SKU)
    );
    """
    curr.execute(books_table)
except Exception as e:
    print(f"Error creating books table: {e}")


#6. Drinks
try:
    drinks_table = """
    CREATE TABLE Drinks(
    DrinkSKU   VARCHAR(4)     NOT NULL,
    Item        VARCHAR(35),
    Price       DECIMAL(4, 2),
    Category    VARCHAR(20),
    Season      VARCHAR(20),
    PRIMARY KEY (DrinkSKU),
    FOREIGN KEY (DrinkSKU) REFERENCES SKUs(SKU)
    );
    """
    curr.execute(drinks_table)
except Exception as e:
    print(f"Error creating drinks table: {e}")


#7. Pastries
try:
    pastries_table = """
    CREATE TABLE Pastries (
    PastrySKU      VARCHAR(4)     NOT NULL,
    PastryName      VARCHAR(40),
    Price           DECIMAL(4, 2),
    Sell_By_Date    DATE,
    PRIMARY KEY (PastrySKU),
    FOREIGN KEY (PastrySKU) REFERENCES SKUs(SKU)
    );
    """
    curr.execute(pastries_table)
except Exception as e:
    print(f"Error creating pastries table: {e}")

#8. Baristas
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


#9. Customer Loyalty
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


#10. Sales
try:
    sales_table = """
            CREATE TABLE Sales (
            Sale_ID             INT     NOT NULL,
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


#11. Sales Item
try:
    sales_item = """
            CREATE TABLE Sales_Item(
            Sale_ID     INT      NOT NULL,
            Item        VARCHAR(11),
            Quantity    INT,
            PRIMARY KEY (Sale_ID, Item),
            FOREIGN KEY (Sale_ID) REFERENCES Sales(Sale_ID),
            FOREIGN KEY (Item) REFERENCES SKUs(SKU)
            );
            """
    curr.execute(sales_item)
except Exception as e:
    print(f"Error creating sales item table: {e}")

#12. Pairs
try:
    pairs = """
            CREATE TABLE Pairs(
            PastrySKU      VARCHAR(4)      NOT NULL,
            DrinkSKU       VARCHAR(4)      NOT NULL,
            SaleDate        DATE            NOT NULL,
            Discount        INT,   
            PRIMARY KEY (PastrySKU, DrinkSKU, SaleDate),
            FOREIGN KEY (PastrySKU) REFERENCES Pastries(PastrySKU),
            FOREIGN KEY (DrinkSKU) REFERENCES Drinks(DrinkSKU)
            );
            """
    curr.execute(pairs)
except Exception as e:
    print(f"Error creating pairs item table: {e}")
    
curr.execute("SHOW TABLES;")
print("Tables: ", curr.fetchall())

curr.close()
conn.close()

