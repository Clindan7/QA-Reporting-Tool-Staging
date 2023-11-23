from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()



BACKLOG_API_KEY = os.environ.get("BACKLOG_API_KEY")
BACKLOG_BASE_URL = os.environ.get("BACKLOG_BASE_URL")
API_KEY =os.environ.get("API_KEY")
SPACE_KEY = os.environ.get("SPACE_KEY")
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('DBHOST'),
            user=os.environ.get('USER_NAME'),
            password=os.environ.get('PASSWORD'),
            database=os.environ.get('DATABASE'),
            port=os.environ.get('PORT')
        )
        print("Database connection established successfully.")
        return connection

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None


