"""
Hashing utilities module for AcademiaVeritas project.

This module provides secure password hashing and certificate integrity verification
functionality using industry-standard cryptographic methods.
"""

import hashlib
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password: str) -> str:
    """
    Securely hash a plain-text password using Werkzeug's password hashing.
    
    This function uses Werkzeug's built-in password hashing which employs
    PBKDF2 with SHA-256 and a random salt for secure password storage.
    
    Args:
        password (str): The plain-text password to be hashed
        
    Returns:
        str: A securely hashed password string that can be safely stored in the database
        
    Example:
        >>> hashed = hash_password("my_secure_password")
        >>> print(hashed)  # Output: pbkdf2:sha256:600000$...
    """
    return generate_password_hash(password)


def check_password(hashed_password: str, password: str) -> bool:
    """
    Verify a plain-text password against its hashed version.
    
    This function securely compares a plain-text password with a hashed password
    using Werkzeug's password checking functionality, which handles timing attacks
    and other security considerations.
    
    Args:
        hashed_password (str): The hashed password stored in the database
        password (str): The plain-text password to verify
        
    Returns:
        bool: True if the password matches the hash, False otherwise
        
    Example:
        >>> stored_hash = "pbkdf2:sha256:600000$..."
        >>> is_valid = check_password(stored_hash, "my_secure_password")
        >>> print(is_valid)  # Output: True or False
    """
    return check_password_hash(hashed_password, password)


def generate_certificate_hash(student_name: str, roll_number: str, course_name: str, issue_date: str) -> str:
    """
    Generate a deterministic SHA-256 hash for certificate data integrity verification.
    
    This function creates a unique, deterministic hash for each certificate by:
    1. Concatenating the input parameters in a fixed order
    2. Converting all inputs to lowercase strings
    3. Separating them with pipe (|) characters
    4. Applying SHA-256 hashing to the resulting string
    
    The resulting hash serves as a unique identifier for the certificate and ensures
    data integrity by detecting any modifications to the certificate data.
    
    Args:
        student_name (str): Full name of the student
        roll_number (str): Student's roll number or ID
        course_name (str): Name of the course or degree program
        issue_date (str): Date when the certificate was issued (YYYY-MM-DD format)
        
    Returns:
        str: A 64-character hexadecimal SHA-256 hash string
        
    Example:
        >>> hash_value = generate_certificate_hash(
        ...     "Jane Doe", 
        ...     "R-98765", 
        ...     "Information Technology", 
        ...     "2025-10-15"
        ... )
        >>> print(hash_value)  # Output: a1b2c3d4e5f6...
        
    Note:
        The input format for issue_date should be consistent (YYYY-MM-DD) to ensure
        deterministic hash generation across different systems.
    """
    # Create a deterministic string by concatenating inputs in fixed order
    # Convert all inputs to lowercase and separate with pipe characters
    certificate_string = f"{student_name.lower()}|{roll_number.lower()}|{course_name.lower()}|{issue_date.lower()}"
    
    # Apply SHA-256 hashing to the concatenated string
    hash_object = hashlib.sha256(certificate_string.encode('utf-8'))
    
    # Return the hexadecimal digest as a string
    return hash_object.hexdigest()
