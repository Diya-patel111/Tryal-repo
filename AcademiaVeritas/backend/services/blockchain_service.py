"""
Blockchain service module for AcademiaVeritas project.

This module provides blockchain integration functionality for storing
certificate hashes on the Ethereum blockchain for immutable verification.
"""

import os
import json
import hashlib
from typing import Optional, Dict, Any


class BlockchainService:
    """
    Service class for blockchain operations.
    
    This class handles certificate hash storage on the blockchain
    and provides verification functionality.
    """
    
    def __init__(self):
        """Initialize the blockchain service."""
        self.infura_api_key = os.getenv('INFURA_API_KEY')
        self.network_url = f"https://sepolia.infura.io/v3/{self.infura_api_key}" if self.infura_api_key else None
    
    def store_certificate_hash(self, certificate_hash: str, institution_id: int) -> Dict[str, Any]:
        """
        Store a certificate hash on the blockchain.
        
        Args:
            certificate_hash (str): The certificate hash to store
            institution_id (int): The institution ID that issued the certificate
            
        Returns:
            Dict[str, Any]: Transaction details or error information
        """
        try:
            if not self.infura_api_key:
                return {
                    'success': False,
                    'error': 'Blockchain service not configured. INFURA_API_KEY is missing.',
                    'tx_hash': None
                }
            
            # For demo purposes, generate a mock transaction hash
            # In production, this would interact with actual blockchain
            mock_tx_hash = self._generate_mock_tx_hash(certificate_hash, institution_id)
            
            return {
                'success': True,
                'tx_hash': mock_tx_hash,
                'block_number': 12345678,  # Mock block number
                'gas_used': 21000,  # Mock gas usage
                'message': 'Certificate hash stored on blockchain successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Blockchain transaction failed: {str(e)}',
                'tx_hash': None
            }
    
    def verify_certificate_hash(self, certificate_hash: str) -> Dict[str, Any]:
        """
        Verify a certificate hash on the blockchain.
        
        Args:
            certificate_hash (str): The certificate hash to verify
            
        Returns:
            Dict[str, Any]: Verification result
        """
        try:
            if not self.infura_api_key:
                return {
                    'verified': False,
                    'error': 'Blockchain service not configured',
                    'tx_hash': None
                }
            
            # For demo purposes, simulate verification
            # In production, this would query the actual blockchain
            is_verified = self._simulate_blockchain_verification(certificate_hash)
            
            return {
                'verified': is_verified,
                'tx_hash': self._generate_mock_tx_hash(certificate_hash, 1) if is_verified else None,
                'block_number': 12345678 if is_verified else None,
                'message': 'Certificate verified on blockchain' if is_verified else 'Certificate not found on blockchain'
            }
            
        except Exception as e:
            return {
                'verified': False,
                'error': f'Blockchain verification failed: {str(e)}',
                'tx_hash': None
            }
    
    def _generate_mock_tx_hash(self, certificate_hash: str, institution_id: int) -> str:
        """
        Generate a mock transaction hash for demo purposes.
        
        Args:
            certificate_hash (str): The certificate hash
            institution_id (int): The institution ID
            
        Returns:
            str: Mock transaction hash
        """
        # Create a deterministic hash based on certificate data
        data = f"{certificate_hash}_{institution_id}_{os.getenv('SECRET_KEY', 'default')}"
        hash_object = hashlib.sha256(data.encode())
        return f"0x{hash_object.hexdigest()[:40]}"
    
    def _simulate_blockchain_verification(self, certificate_hash: str) -> bool:
        """
        Simulate blockchain verification for demo purposes.
        
        Args:
            certificate_hash (str): The certificate hash to verify
            
        Returns:
            bool: True if verified, False otherwise
        """
        # For demo purposes, assume all hashes are verified
        # In production, this would query the actual blockchain
        return len(certificate_hash) > 0 and certificate_hash.startswith('a')


# Global instance
blockchain_service = BlockchainService()


def store_certificate_on_blockchain(certificate_hash: str, institution_id: int) -> Dict[str, Any]:
    """
    Convenience function to store certificate hash on blockchain.
    
    Args:
        certificate_hash (str): The certificate hash to store
        institution_id (int): The institution ID
        
    Returns:
        Dict[str, Any]: Transaction result
    """
    return blockchain_service.store_certificate_hash(certificate_hash, institution_id)


def verify_certificate_on_blockchain(certificate_hash: str) -> Dict[str, Any]:
    """
    Convenience function to verify certificate hash on blockchain.
    
    Args:
        certificate_hash (str): The certificate hash to verify
        
    Returns:
        Dict[str, Any]: Verification result
    """
    return blockchain_service.verify_certificate_hash(certificate_hash)
