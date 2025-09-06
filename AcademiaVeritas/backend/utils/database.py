"""
Database connection module for AcademiaVeritas project.

This module provides database connectivity functionality for the Flask backend,
handling PostgreSQL connections with proper error handling and environment configuration.
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database using environment variables.
    
    This function reads the DATABASE_URL from environment variables and attempts
    to establish a connection to the PostgreSQL database. It includes comprehensive
    error handling to gracefully manage connection failures.
    
    Returns:
        psycopg2.connection: Database connection object on success
        None: Returns None if connection fails
        
    Raises:
        No exceptions are raised - all errors are caught and handled gracefully
    """
    try:
        # Read database URL from environment variables
        database_url = os.getenv('DATABASE_URL')
        
        # Validate that DATABASE_URL is set
        if not database_url:
            print("Error: DATABASE_URL environment variable is not set")
            return None
        
        # Establish connection to PostgreSQL database
        connection = psycopg2.connect(database_url)
        
        # Print success message for debugging (remove in production)
        print("Successfully connected to PostgreSQL database")
        
        return connection
        
    except psycopg2.OperationalError as e:
        # Handle database connection errors (invalid credentials, server down, etc.)
        print(f"Database connection error: {e}")
        print("Please check your DATABASE_URL configuration and ensure PostgreSQL is running")
        return None
        
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error occurred while connecting to database: {e}")
        return None


def close_db_connection(connection):
    """
    Safely closes a database connection.
    
    Args:
        connection: psycopg2 connection object to close
    """
    if connection:
        try:
            connection.close()
            print("Database connection closed successfully")
        except Exception as e:
            print(f"Error closing database connection: {e}")


def test_db_connection():
    """
    Test function to verify database connectivity.
    
    This function can be used during development to test if the database
    connection is working properly.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    connection = get_db_connection()
    if connection:
        close_db_connection(connection)
        return True
    return False
