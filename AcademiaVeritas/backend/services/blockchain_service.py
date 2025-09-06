"""
Blockchain service module for AcademiaVeritas project.

This module provides Web3 integration for interacting with the CertificateRegistry
smart contract on the Ethereum blockchain for immutable certificate verification.
"""

import os
import json
from typing import Optional
from web3 import Web3
from web3.exceptions import ContractLogicError, TransactionNotFound, TimeExhausted


class BlockchainService:
    """
    Service class for blockchain operations using Web3.py.
    
    This class handles certificate hash storage and verification on the Ethereum
    blockchain through the deployed CertificateRegistry smart contract.
    """
    
    def __init__(self):
        """Initialize the blockchain service with Web3 provider and contract."""
        # Load environment variables
        self.infura_api_key = os.getenv('INFURA_API_KEY')
        self.contract_address = os.getenv('CONTRACT_ADDRESS')
        self.wallet_private_key = os.getenv('WALLET_PRIVATE_KEY')
        self.wallet_address = os.getenv('WALLET_ADDRESS')
        
        # Validate required environment variables
        if not all([self.infura_api_key, self.contract_address, self.wallet_private_key, self.wallet_address]):
            raise ValueError(
                "Missing required environment variables. Please set: "
                "INFURA_API_KEY, CONTRACT_ADDRESS, WALLET_PRIVATE_KEY, WALLET_ADDRESS"
            )
        
        # Initialize Web3 provider
        self.network_url = f"https://sepolia.infura.io/v3/{self.infura_api_key}"
        self.w3 = Web3(Web3.HTTPProvider(self.network_url))
        
        # Verify connection to blockchain
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum network")
        
        # Load contract ABI
        self.contract_abi = self._load_contract_abi()
        
        # Create contract instance
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )
        
        # Set default account for transactions
        self.w3.eth.default_account = self.wallet_address
    
    def _load_contract_abi(self) -> list:
        """
        Load the contract ABI from the JSON file.
        
        Returns:
            list: The contract ABI as a Python list
            
        Raises:
            FileNotFoundError: If the ABI file is not found
            json.JSONDecodeError: If the ABI file contains invalid JSON
        """
        abi_path = os.path.join(os.path.dirname(__file__), 'CertificateRegistry.json')
        
        try:
            with open(abi_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Contract ABI file not found at {abi_path}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in ABI file: {e}")
    
    def verify_hash(self, certificate_hash: str) -> bool:
        """
        Verify if a certificate hash exists on the blockchain.
        
        This function performs a read-only check against the smart contract
        to determine if the certificate hash has been registered.
        
        Args:
            certificate_hash (str): The certificate hash as a hex string
            
        Returns:
            bool: True if the hash is verified on blockchain, False otherwise
            
        Raises:
            ValueError: If the certificate hash format is invalid
        """
        try:
            # Validate and convert hex string to bytes32
            if not certificate_hash.startswith('0x'):
                certificate_hash = '0x' + certificate_hash
            
            # Convert hex string to bytes32
            hash_bytes = bytes.fromhex(certificate_hash[2:])  # Remove '0x' prefix
            
            if len(hash_bytes) != 32:
                raise ValueError("Certificate hash must be 32 bytes (64 hex characters)")
            
            # Call the smart contract's isVerified function
            is_verified = self.contract.functions.isVerified(hash_bytes).call()
            
            return is_verified
            
        except ValueError as e:
            print(f"Invalid certificate hash format: {e}")
            return False
        except Exception as e:
            print(f"Error verifying hash on blockchain: {e}")
            return False
    
    def add_hash(self, certificate_hash: str) -> Optional[str]:
        """
        Add a certificate hash to the blockchain registry.
        
        This function creates and sends a transaction to the smart contract
        to register a new certificate hash on the blockchain.
        
        Args:
            certificate_hash (str): The certificate hash as a hex string
            
        Returns:
            Optional[str]: Transaction hash if successful, None if failed
            
        Raises:
            ValueError: If the certificate hash format is invalid
        """
        try:
            # Validate and convert hex string to bytes32
            if not certificate_hash.startswith('0x'):
                certificate_hash = '0x' + certificate_hash
            
            # Convert hex string to bytes32
            hash_bytes = bytes.fromhex(certificate_hash[2:])  # Remove '0x' prefix
            
            if len(hash_bytes) != 32:
                raise ValueError("Certificate hash must be 32 bytes (64 hex characters)")
            
            # Get current gas price
            gas_price = self.w3.eth.gas_price
            
            # Get nonce for the transaction
            nonce = self.w3.eth.get_transaction_count(self.wallet_address)
            
            # Build the transaction
            transaction = self.contract.functions.addCertificateHash(hash_bytes).build_transaction({
                'chainId': 11155111,  # Sepolia testnet chain ID
                'from': self.wallet_address,
                'gasPrice': gas_price,
                'nonce': nonce,
            })
            
            # Estimate gas for the transaction
            try:
                gas_estimate = self.contract.functions.addCertificateHash(hash_bytes).estimate_gas({
                    'from': self.wallet_address
                })
                transaction['gas'] = gas_estimate
            except ContractLogicError as e:
                if "already exists" in str(e):
                    print(f"Certificate hash already exists on blockchain: {certificate_hash}")
                    return None
                else:
                    print(f"Contract logic error: {e}")
                    return None
            
            # Sign the transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.wallet_private_key)
            
            # Send the raw transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            try:
                receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
                
                if receipt.status == 1:
                    print(f"Certificate hash successfully added to blockchain: {tx_hash.hex()}")
                    return tx_hash.hex()
                else:
                    print(f"Transaction failed: {tx_hash.hex()}")
                    return None
                    
            except TimeExhausted:
                print(f"Transaction timeout: {tx_hash.hex()}")
                return None
            except TransactionNotFound:
                print(f"Transaction not found: {tx_hash.hex()}")
                return None
                
        except ValueError as e:
            print(f"Invalid certificate hash format: {e}")
            return None
        except ContractLogicError as e:
            if "already exists" in str(e):
                print(f"Certificate hash already exists on blockchain: {certificate_hash}")
                return None
            else:
                print(f"Contract logic error: {e}")
                return None
        except Exception as e:
            print(f"Error adding hash to blockchain: {e}")
            return None


# Global instance
try:
    blockchain_service = BlockchainService()
except (ValueError, ConnectionError, FileNotFoundError) as e:
    print(f"Blockchain service initialization failed: {e}")
    blockchain_service = None


def verify_hash(certificate_hash: str) -> bool:
    """
    Convenience function to verify a certificate hash on the blockchain.
    
    Args:
        certificate_hash (str): The certificate hash to verify
        
    Returns:
        bool: True if verified, False otherwise
    """
    if blockchain_service is None:
        print("Blockchain service not available")
        return False
    
    return blockchain_service.verify_hash(certificate_hash)


def add_hash(certificate_hash: str) -> Optional[str]:
    """
    Convenience function to add a certificate hash to the blockchain.
    
    Args:
        certificate_hash (str): The certificate hash to add
        
    Returns:
        Optional[str]: Transaction hash if successful, None otherwise
    """
    if blockchain_service is None:
        print("Blockchain service not available")
        return None
    
    return blockchain_service.add_hash(certificate_hash)