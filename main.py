import mysql.connector
from mysql.connector import Error

def run_mysql_demo():
    print("Welcome User!! This Program connects to any database whether it is running on the localHost or on a remote server.\n")
    connection = None
    cursor = None
    try:
        # 1. Establishing the connection
        connection = mysql.connector.connect(
            host=str(input("Enter HostName:")),
            user= str(input("Enter Username:")),        
            password=str(input("Enter Password:")), 
            database=str(input("Enter Database Name:")),  
            port = int(input("Enter Port Number (Default is 3306:)"))
        )

        if connection.is_connected():
            print(" \n")
            print("\nSuccessfully connected to the MySQL database.")
            cursor = connection.cursor()

            # 2. Creating a Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL
                )
            """)
            print("Table 'users' verified/created.")

            # 3. Executing an Insert Statement
            insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
            user_data = ("Alice Smith", "alice@example.com")
            
            try:
                cursor.execute(insert_query, user_data)
                # Commit changes for data modifications (DML)
                connection.commit() 
                print(f"Inserted row ID: {cursor.lastrowid}")
            except Error as insert_err:
                print(f"Skipping insert (likely duplicate email): {insert_err}")

            # 4. Execute a Read Query (SELECT)
            cursor.execute("SELECT id, name, email FROM users")
            
            # Fetch all rows from the last executed query
            rows = cursor.fetchall()
            print("\n--- User Records ---")
            for row in rows:
                print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]}")

    except Error as e:
        print(f"Database error occurred: {e}")
        
    finally:
        # 5. Cleaning up our database and closing the connection
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("\nMySQL connection closed.")

if __name__ == "__main__":
    run_mysql_demo()
