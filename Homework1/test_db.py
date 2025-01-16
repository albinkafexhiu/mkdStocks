from src.database.db_manager import DatabaseManager

def test_connection():
    db = DatabaseManager()
    if db.test_connection():
        print("Successfully connected to the database!")
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    test_connection()