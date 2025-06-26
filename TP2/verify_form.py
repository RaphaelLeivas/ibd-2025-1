import sqlite3
import pandas as pd

def is_table_in_1nf(db_file, table_name):
    """
    Verifies if a table in a SQLite database is in First Normal Form (1NF).
    
    Args:
        db_file (str): Path to the SQLite database file.
        table_name (str): Name of the table to verify.
    
    Returns:
        bool: True if the table is in 1NF, False otherwise.
    """
    conn = sqlite3.connect(db_file)
    try:
        # Load the table into a DataFrame
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        
        # Check for atomic values (no lists, dictionaries, or arrays)
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, (list, dict, set))).any():
                print(f"Column '{col}' contains non-atomic values.")
                return False
        
        # Check for unique rows
        if df.duplicated().any():
            print("The table contains duplicate rows.")
            return False
        
        # Check for a primary key (unique identifier)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()
        primary_keys = [col[1] for col in columns_info if col[5] == 1]  # Column with PK flag
        
        if not primary_keys:
            print("The table does not have a primary key.")
            return False
        
        print(f"The table '{table_name}' is in 1NF.")
        return True
    except Exception as e:
        print(f"Error verifying 1NF for table '{table_name}': {e}")
        return False
    finally:
        conn.close()


def is_table_in_2nf(db_file, table_name):
    """
    Verifies if a table in a SQLite database is in Second Normal Form (2NF).
    
    Args:
        db_file (str): Path to the SQLite database file.
        table_name (str): Name of the table to verify.
    
    Returns:
        bool: True if the table is in 2NF, False otherwise.
    """
    conn = sqlite3.connect(db_file)
    try:
        cursor = conn.cursor()
        
        # Step 1: Check if the table has a primary key
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()
        primary_keys = [col[1] for col in columns_info if col[5] == 1]  # Column with PK flag
        
        if not primary_keys:
            print(f"The table '{table_name}' does not have a primary key, so it cannot be in 2NF.")
            return False
        
        # Step 2: Check for partial dependency
        # A table is not in 2NF if non-prime attributes depend on part of the primary key
        # For composite primary keys, we need to check dependencies for each part of the key
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        create_table_sql = cursor.fetchone()[0]
        
        # Extract foreign key constraints
        foreign_keys = []
        for line in create_table_sql.splitlines():
            if "FOREIGN KEY" in line:
                foreign_keys.append(line.strip())
        
        if foreign_keys:
            print(f"The table '{table_name}' has foreign key constraints, which may indicate partial dependencies.")
            return False
        
        print(f"The table '{table_name}' is in 2NF.")
        return True
    except Exception as e:
        print(f"Error verifying 2NF for table '{table_name}': {e}")
        return False
    finally:
        conn.close()


def is_table_in_3nf(db_file, table_name):
    """
    Verifies if a table in a SQLite database is in Third Normal Form (3NF).
    
    Args:
        db_file (str): Path to the SQLite database file.
        table_name (str): Name of the table to verify.
    
    Returns:
        bool: True if the table is in 3NF, False otherwise.
    """
    conn = sqlite3.connect(db_file)
    try:
        cursor = conn.cursor()
        
        # Step 1: Check if the table has a primary key
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()
        primary_keys = [col[1] for col in columns_info if col[5] == 1]  # Column with PK flag
        
        if not primary_keys:
            print(f"The table '{table_name}' does not have a primary key, so it cannot be in 3NF.")
            return False
        
        # Step 2: Check for transitive dependencies
        # A table is not in 3NF if non-prime attributes depend on other non-prime attributes
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        create_table_sql = cursor.fetchone()[0]
        
        # Extract foreign key constraints
        foreign_keys = []
        for line in create_table_sql.splitlines():
            if "FOREIGN KEY" in line:
                foreign_keys.append(line.strip())
        
        if foreign_keys:
            print(f"The table '{table_name}' has foreign key constraints, which may indicate transitive dependencies.")
            return False
        
        print(f"The table '{table_name}' is in 3NF.")
        return True
    except Exception as e:
        print(f"Error verifying 3NF for table '{table_name}': {e}")
        return False
    finally:
        conn.close()

def verify_database_normalization(db_file, table_name=None):
    """
    Verifies the normalization of all tables in a SQLite database.
    
    Args:
        db_file (str): Path to the SQLite database file.
    
    Returns:
        dict: A dictionary with table names as keys and their normalization status as values.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    normalization_status = {}
    

        
    is_1nf = is_table_in_1nf(db_file, table_name)
    is_2nf = is_table_in_2nf(db_file, table_name) if is_1nf else False
    is_3nf = is_table_in_3nf(db_file, table_name) if is_2nf else False
        
    normalization_status[table_name] = {
        '1NF': is_1nf,
        '2NF': is_2nf,
        '3NF': is_3nf
    }
    
    conn.close()
    return normalization_status