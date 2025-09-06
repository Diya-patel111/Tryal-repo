"""
Configuration module for AcademiaVeritas project.

This module handles application configuration, environment variables,
and database settings for the Flask backend.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class with common settings."""
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/academia_veritas')
    
    # Blockchain
    INFURA_API_KEY = os.getenv('INFURA_API_KEY', '')
    CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', '')
    WALLET_PRIVATE_KEY = os.getenv('WALLET_PRIVATE_KEY', '')
    WALLET_ADDRESS = os.getenv('WALLET_ADDRESS', '')
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
    
    # JWT Settings
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = 24
    
    # CORS Settings
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5173']


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv('TEST_DATABASE_URL', 'postgresql://user:password@localhost:5432/academia_veritas_test')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
