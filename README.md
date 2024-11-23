1. **`pyscriptsTables/`**  
   - Has the scripts for how I made each table. If they need edits eventually, you will have to change the links to the correct dirs.

2. **`menu/`**  
   - Contains old CSV files of menus:
     - **Food menu**: real data
     - **Drink and Pastry menus**: Mix of real and fake data.
     - Didn't use the wine and beer menus, but if anyone wants to clean those up we can.

3. **`pyScriptsDB/`**  
   - Contains the Python scripts for working with the database:
   - (Run them in this order, as long as you connect to your db with your password, you shouldnt have to change anything)
     1. **`dbSetup.py`**: Sets up the database and tables.
     2. **`insertData.py`**: Inserts data into the tables.
     3. **`Queries.py`**: Runs our queries.
     4. **`dbTeardown.py`**: Cleans up the database (drops tables and the database).
     5. **`pyScriptsDB/tables`**:
       - Contains the CSV files that populate the database (that were created in pyscriptsTables)

  - We will still need customer and barista tables, as well as allergens and the purchase table. 
  These will be randomly generated (?) so anyone can make those.
  
  - Some of the tables (like ingredients) dont have everything we listed on the ER, but that was a lower priorty for me bc that can just be changed later.

  Lmk if u have questions!


