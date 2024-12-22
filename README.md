# Café and Bookstore Database Project

This repository contains the final project for our database design course. We created a relational database to simulate daily operations for a local café and bookstore, modeled after **Plein Air**.

## Project Description
- **Goal**: Optimize workflows by designing a database that supports menu management, sales tracking, and customer loyalty programs.
- **Implementation**:
  - Designed an **ER diagram** to model entities like goods (menu items, pastries, drinks, books), baristas, sales, and customer loyalty.
  - Populated tables with real and generated data sourced from:
    - [Plein Air Café](http://www.pleinaircafe.co)
    - [Kaggle Book Dataset](https://www.kaggle.com/datasets/middlelight)
  - Developed a relational schema optimized for efficient querying, reducing unnecessary joins by denormalizing frequently accessed attributes.

## Key Features
- Tracks goods sold, including books, pastries, drinks, and menu items.
- Records barista sales, customer loyalty participation, and daily transactions.
- Supports discounts for paired items (e.g., fall beverages and pastries).

## Implementation Highlights
- **Tools**: MySQL for database implementation, Python for data cleaning and integration.

## Repository Structure

- **pyScriptsDB/**: Contains Python scripts for the setup and implementation of the Database including:
    - **`dbSetup.py`**: Creates the database and tables via mysql.connector
    - **`insertData.py`**: Script to populate tables with data via my sql.connector.
    - **`dbTeardown.py`**: Deletes all tables and database via my sql.connector.
    - **`app.py`**: Flask application script that provides a user interface for interacting with the database
- **pyScriptsTables/**: Contains Python scripts to generate files for all database tables using a combination of real and generated data

## Contributors
- **Emma Griffin**  
- **Olivia Werba**

---

For more details, refer to our final presentation [here](https://github.com/ecg1331/db_autumn2024/blob/main/Final12_10_24.pdf).



