import os
import pyodbc
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Database configuration and connection management"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '1433')
        self.database = os.getenv('DB_NAME', 'SentimentDB')
        self.username = os.getenv('DB_USER', 'sa')
        self.password = os.getenv('DB_PASSWORD')
        
        if not self.password:
            raise ValueError("DB_PASSWORD environment variable is required")
    
    def get_connection_string(self) -> str:
        """Get ODBC connection string"""
        return (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.host},{self.port};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
            f"TrustServerCertificate=yes;"
        )
    
    def get_connection(self) -> Optional[pyodbc.Connection]:
        """Get database connection"""
        try:
            connection_string = self.get_connection_string()
            connection = pyodbc.connect(connection_string)
            logger.info("Database connection established successfully")
            return connection
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            conn = self.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                conn.close()
                return result is not None
            return False
        except Exception as e:
            logger.error(f"Database connection test failed: {str(e)}")
            return False

# Global database configuration instance
db_config = DatabaseConfig()

