import pandas as pd
import mysql.connector

# establishing connection
conn = mysql.connector.connect(user = 'root',
                               password = ' ',
                               host = 'localhost',
                               database = 'MyCoffeeShop'
                               )
print(conn)
curr = conn.cursor()

'''
Most of these are really simple, but theyre just to test
'''

# Listing ingredients for V Chicken Baguette
query = """
SELECT M.ItemName, I.IngredientName
FROM Recipes as R
JOIN Menu AS M ON R.MenuItemSkew = M.MenuItemSkew
JOIN Ingredients AS I ON R.IngredientSkew = I.IngredientSkew
WHERE M.ItemName = 'Vegan Chicken Baguette';
"""

curr.execute(query)
print(curr.fetchall())
print("-"*50)

# Counting ingredients for each item
query2 = """
SELECT M.ItemName, COUNT(I.IngredientName) AS IngredientCount
FROM Recipes AS R
JOIN Menu AS M ON R.MenuItemSkew = M.MenuItemSkew
JOIN Ingredients AS I ON R.IngredientSkew = I.IngredientSkew
GROUP BY M.ItemName
ORDER BY M.ItemName;
"""
curr.execute(query2)
print(curr.fetchall())
print("-"*50)

# Counting ingredients for each item
query2 = """
SELECT M.ItemName, COUNT(I.IngredientName) AS IngredientCount
FROM Recipes AS R
JOIN Menu AS M ON R.MenuItemSkew = M.MenuItemSkew
JOIN Ingredients AS I ON R.IngredientSkew = I.IngredientSkew
GROUP BY M.ItemName
ORDER BY M.ItemName;
"""
curr.execute(query2)
print(curr.fetchall())
print("-"*50)


# Menu items where catagory = breakfast
query3 = """
SELECT ItemName
FROM Menu
WHERE Category = 'Breakfast';
"""
curr.execute(query3)
print(curr.fetchall())
print("-"*50)


# books with fantasy genre
query4 = """
SELECT Title
FROM Books
WHERE Genre = 'Fantasy'
LIMIT 10;
"""
curr.execute(query4)
print(curr.fetchall())
print("-"*50)

# fall drinks
query5 = """
SELECT Item, Price
FROM Drinks
WHERE Season = 'Fall';
"""
curr.execute(query5)
print(curr.fetchall())
print("-"*50)


# vegan pastries (can do this instead of allergens)
query6 = """
SELECT PastryName
FROM Pastries
WHERE PastryName LIKE 'vegan%';
"""
curr.execute(query6)
print(curr.fetchall())
print("-"*50)


# fantasy books bought in 2023
query7 = """
SELECT B.Title, B.Genre
FROM Books as B
JOIN Skews AS S ON S.Skew = B.ISBN
JOIN Sales_Item AS SI on SI.Item = S.Skew
JOIN Sales AS SAL on SAL.Sale_ID = SI.Sale_ID
WHERE B. Genre = 'Fantasy' AND YEAR(SAL.Sale_Date) = 2023;
"""
curr.execute(query7)
print(curr.fetchall())
print("-"*50)

# month with the most sales
query8 = """
SELECT MONTH(Sale_Date)"""


curr.close()
conn.close()