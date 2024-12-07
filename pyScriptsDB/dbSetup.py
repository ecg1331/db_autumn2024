import pandas as pd
import mysql.connector
from datetime import datetime

# establishing connection
conn = mysql.connector.connect(user = 'root',
                               password = '',
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

# 1. Skews Table
try:
    skew_table = """
            CREATE TABLE Skews(
            Skew     VARCHAR(10)      NOT NULL,
            Price     DECIMAL(4, 2),    
            PRIMARY KEY (Skew)
            );
            """
    curr.execute(skew_table)
except Exception as e:
    print(f"Error creating skew table: {e}")

#2. Menu
try:
    menu_query = """
        CREATE TABLE Menu (
            MenuItemSkew VARCHAR(4)    NOT NULL,
            ItemName    VARCHAR(45),
            Category    VARCHAR(35),
            Price       DECIMAL(4, 2),
            PRIMARY KEY (MenuItemSkew),
            FOREIGN KEY (MenuItemSkew) REFERENCES Skews(Skew)
            );
            """
    curr.execute(menu_query)
except Exception as e:
    print(f"Errror creating menu table: {e}")

#3. Ingredients
try:
    ingredient_table = """
        CREATE TABLE Ingredients (
            IngredientSkew      VARCHAR(4)    NOT NULL,
            IngredientName      VARCHAR(30),
            PRIMARY KEY (IngredientSkew)
            );
            """
    curr.execute(ingredient_table)
except Exception as e:
    print(f"Errror creating ingredient table: {e}")


#4. Recipies
try:
    recipe_table = """
        CREATE TABLE Recipes (
            MenuItemSkew VARCHAR(4) NOT NULL,
            IngredientSkew VARCHAR(4) NOT NULL,
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
        FOREIGN KEY (ISBN) REFERENCES Skews(Skew)
    );
    """
    curr.execute(books_table)
except Exception as e:
    print(f"Error creating books table: {e}")


#6. Drinks
try:
    drinks_table = """
    CREATE TABLE Drinks(
    DrinkSkew   VARCHAR(4)     NOT NULL,
    Item        VARCHAR(35),
    Price       DECIMAL(4, 2),
    Category    VARCHAR(20),
    Season      VARCHAR(20),
    PRIMARY KEY (DrinkSkew),
    FOREIGN KEY (DrinkSkew) REFERENCES Skews(Skew)
    );
    """
    curr.execute(drinks_table)
except Exception as e:
    print(f"Error creating drinks table: {e}")


#7. Pastries
try:
    pastries_table = """
    CREATE TABLE Pastries (
    PastrySkew      VARCHAR(4)     NOT NULL,
    PastryName      VARCHAR(40),
    Price           DECIMAL(4, 2),
    Sell_By_Date    DATE,
    PRIMARY KEY (PastrySkew),
    FOREIGN KEY (PastrySkew) REFERENCES Skews(Skew)
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
            FOREIGN KEY (Item) REFERENCES Skews(Skew)
            );
            """
    curr.execute(sales_item)
except Exception as e:
    print(f"Error creating sales item table: {e}")

#12. Pairs
try:
    pairs = """
            CREATE TABLE Pairs(
            PastrySkew      VARCHAR(4)      NOT NULL,
            DrinkSkew       VARCHAR(4)      NOT NULL,
            SaleDate        DATE            NOT NULL,
            Discount        INT,   
            PRIMARY KEY (PastrySkew, DrinkSkew, SaleDate),
            FOREIGN KEY (PastrySkew) REFERENCES Pastries(PastrySkew),
            FOREIGN KEY (DrinkSkew) REFERENCES Drinks(DrinkSkew)
            );
            """
    curr.execute(pairs)
except Exception as e:
    print(f"Error creating pairs item table: {e}")
    
curr.execute("SHOW TABLES;")
print("Tables: ", curr.fetchall())

curr.close()
conn.close()

