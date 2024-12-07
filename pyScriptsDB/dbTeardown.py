import mysql.connector

# establishing connection
conn = mysql.connector.connect(user = 'root',
                               password = '',
                               host = 'localhost',
                               )

curr = conn.cursor()

try:
    curr.execute("DROP DATABASE MyCoffeeShop;")
    print("Database successfully dropped")
except Exception as e:
    print("Error dropping database:", {e})

finally:
    curr.close()
    conn.close()