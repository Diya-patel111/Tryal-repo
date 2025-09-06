# Blockchain Integration Documentation

## Overview

The AcademiaVeritas project now includes a robust two-factor verification system that combines traditional database storage with immutable blockchain verification. This integration provides an additional layer of security and tamper-proof verification for academic certificates.

## Architecture

### Two-Factor Verification System

1. **Factor 1: Database Verification**
   - Certificate data is stored in PostgreSQL database
   - Provides fast querying and relational data management
   - Includes institution relationships and metadata

2. **Factor 2: Blockchain Verification**
   - Certificate hashes are stored on Ethereum blockchain
   - Provides immutable, tamper-proof verification
   - Uses smart contract for decentralized verification

## Components

### 1. Smart Contract (`CertificateRegistry.sol`)

**Location**: `blockchain/contracts/CertificateRegistry.sol`

**Features**:
- Inherits from OpenZeppelin's `Ownable` for secure access control
- Stores certificate hashes in a `mapping(bytes32 => bool)`
- Provides `addCertificateHash()` function for owner-only hash registration
- Provides `isVerified()` view function for public verification
- Emits `HashAdded` event for off-chain monitoring

**Security Features**:
- Only contract owner can add new hashes
- Prevents duplicate hash entries
- Gas-optimized for cost efficiency
- Immutable once deployed

### 2. Blockchain Service (`blockchain_service.py`)

**Location**: `backend/services/blockchain_service.py`

**Dependencies**:
- `web3==6.11.3` for Ethereum interaction
- Contract ABI from `CertificateRegistry.json`

**Key Functions**:

#### `verify_hash(certificate_hash: str) -> bool`
- Performs read-only verification against smart contract
- Converts hex string to bytes32 format
- Returns `True` if hash exists on blockchain, `False` otherwise
- Handles errors gracefully with comprehensive exception handling

#### `add_hash(certificate_hash: str) -> Optional[str]`
- Creates and sends transaction to smart contract
- Signs transaction with wallet private key
- Waits for transaction confirmation
- Returns transaction hash on success, `None` on failure
- Handles duplicate hash errors and transaction failures

**Configuration Requirements**:
```env
INFURA_API_KEY=your-infura-api-key
CONTRACT_ADDRESS=0x...your-contract-address
WALLET_PRIVATE_KEY=0x...your-private-key
WALLET_ADDRESS=0x...your-wallet-address
```

### 3. API Integration

**Modified Endpoints**:

#### `POST /api/certificate/add`
- **Before**: Only stored certificate in database
- **After**: Stores in database AND registers hash on blockchain
- **Response**: Includes `blockchain_tx_hash` if successful
- **Error Handling**: Continues with database storage even if blockchain fails

#### `POST /api/verify`
- **Before**: Only checked database for certificate
- **After**: Performs two-factor verification
- **Verification Logic**:
  - Database check (Factor 1)
  - Blockchain verification (Factor 2)
- **Response Statuses**:
  - `VERIFIED_ON_CHAIN`: Both factors pass
  - `RECORD_FOUND_BUT_NOT_ON_CHAIN`: Database only
  - `NOT_FOUND`: Neither factor passes

## Setup Instructions

### 1. Environment Configuration

Create a `.env` file in the backend directory:

```env
# Existing configuration
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/academia_veritas

# New blockchain configuration
INFURA_API_KEY=your-infura-api-key-here
CONTRACT_ADDRESS=your-deployed-contract-address-here
WALLET_PRIVATE_KEY=your-ethereum-wallet-private-key-here
WALLET_ADDRESS=your-ethereum-wallet-public-address-here
```

### 2. Smart Contract Deployment

1. Deploy `CertificateRegistry.sol` to Ethereum Sepolia testnet
2. Update `CONTRACT_ADDRESS` in `.env` with deployed address
3. Ensure wallet has sufficient ETH for gas fees

### 3. Dependencies Installation

```bash
cd backend
pip install -r requirements.txt
```

### 4. Contract ABI

The `CertificateRegistry.json` file contains the compiled contract ABI and is automatically loaded by the blockchain service.

## Security Considerations

### 1. Private Key Management
- Store private keys securely (use environment variables)
- Consider using hardware wallets for production
- Never commit private keys to version control

### 2. Gas Management
- Monitor gas prices for cost optimization
- Implement gas estimation before transactions
- Handle transaction failures gracefully

### 3. Error Handling
- Comprehensive exception handling for network issues
- Graceful degradation when blockchain is unavailable
- Logging for debugging and monitoring

### 4. Access Control
- Only contract owner can add new hashes
- Public verification is read-only
- No sensitive data stored on blockchain

## Verification Flow

### Certificate Addition Flow

1. Institution submits certificate data
2. System generates SHA-256 hash of certificate details
3. Hash is stored in database
4. Hash is registered on blockchain (if successful)
5. Response includes both database ID and transaction hash

### Certificate Verification Flow

1. User uploads certificate image
2. OCR extracts certificate details
3. System generates hash from extracted details
4. **Factor 1**: Check database for matching hash
5. **Factor 2**: Verify hash exists on blockchain
6. Return verification status based on both factors

## Error Handling

### Blockchain Service Errors
- Network connectivity issues
- Invalid contract address or ABI
- Insufficient gas for transactions
- Duplicate hash attempts
- Transaction timeouts

### API Error Responses
- Graceful degradation when blockchain unavailable
- Clear error messages for debugging
- Fallback to database-only verification
- Warning messages for partial verification

## Monitoring and Logging

### Recommended Monitoring
- Transaction success/failure rates
- Gas usage patterns
- Network connectivity status
- Verification response times

### Logging Points
- Blockchain service initialization
- Transaction attempts and results
- Verification requests and responses
- Error conditions and recovery

## Production Considerations

### 1. Network Selection
- Use mainnet for production certificates
- Consider layer 2 solutions for cost reduction
- Implement network switching for testing

### 2. Scalability
- Monitor gas costs as volume increases
- Consider batch operations for efficiency
- Implement caching for frequent verifications

### 3. Backup and Recovery
- Maintain database backups
- Document contract addresses and ABIs
- Plan for contract upgrades if needed

## Testing

### Unit Tests
- Test blockchain service functions
- Mock Web3 responses for testing
- Test error handling scenarios

### Integration Tests
- Test full verification flow
- Test with actual testnet contracts
- Verify two-factor verification logic

### Load Testing
- Test with high verification volumes
- Monitor gas usage patterns
- Test network failure scenarios

## Troubleshooting

### Common Issues

1. **"Blockchain service not available"**
   - Check environment variables
   - Verify network connectivity
   - Check contract address validity

2. **"Transaction failed"**
   - Check wallet balance for gas
   - Verify private key format
   - Check gas price settings

3. **"Certificate hash already exists"**
   - Normal behavior for duplicate certificates
   - Check if hash was previously registered
   - Verify hash generation logic

### Debug Commands

```python
# Test blockchain connection
from services.blockchain_service import blockchain_service
print(blockchain_service.w3.is_connected())

# Test contract interaction
from services.blockchain_service import verify_hash
result = verify_hash("0x...your-hash-here")
print(f"Verification result: {result}")
```

## Future Enhancements

### Potential Improvements
1. **Batch Operations**: Add multiple hashes in single transaction
2. **Event Monitoring**: Real-time verification status updates
3. **Multi-Chain Support**: Support for other blockchain networks
4. **Gas Optimization**: Implement gas price prediction
5. **Analytics Dashboard**: Monitor verification patterns and costs

### Integration Opportunities
1. **IPFS Storage**: Store certificate metadata on IPFS
2. **NFT Integration**: Create NFT representations of certificates
3. **Cross-Chain Verification**: Verify across multiple networks
4. **Smart Contract Upgrades**: Implement upgradeable contracts

---

This blockchain integration provides a robust, secure, and scalable foundation for academic certificate verification while maintaining the flexibility and performance of traditional database systems.

