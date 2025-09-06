// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title CertificateRegistry
 * @author AcademiaVeritas Team
 * @notice A secure, immutable registry for verified academic certificate hashes
 * @dev This contract provides a tamper-proof on-chain registry for academic certificates
 *      by storing SHA-256 hashes of verified certificates. Only the contract owner
 *      can add new certificate hashes to prevent unauthorized entries.
 * 
 * @custom:security This contract inherits from OpenZeppelin's Ownable for secure
 *                  ownership management and access control.
 */
contract CertificateRegistry is Ownable {
    
    /**
     * @notice Mapping to store verified certificate hashes
     * @dev Maps certificate hash (bytes32) to verification status (bool)
     *      true = verified and registered, false = not verified
     */
    mapping(bytes32 => bool) public verifiedHashes;
    
    /**
     * @notice Event emitted when a new certificate hash is successfully added
     * @param certificateHash The SHA-256 hash of the verified certificate
     * @dev This event enables off-chain monitoring and indexing of new registrations
     */
    event HashAdded(bytes32 indexed certificateHash);
    
    /**
     * @notice Constructor that sets the initial owner of the contract
     * @dev Calls the Ownable constructor to set the deployer as the initial owner
     */
    constructor() Ownable(msg.sender) {}
    
    /**
     * @notice Adds a new verified certificate hash to the registry
     * @param _certificateHash The SHA-256 hash of the certificate to be registered
     * @dev This function is restricted to the contract owner only
     * @dev Prevents duplicate entries by checking if hash already exists
     * @dev Emits HashAdded event upon successful registration
     * 
     * Requirements:
     * - Only the contract owner can call this function
     * - The certificate hash must not already exist in the registry
     * 
     * @custom:security Uses onlyOwner modifier for access control
     * @custom:gas-optimization Simple state update with minimal gas consumption
     */
    function addCertificateHash(bytes32 _certificateHash) public onlyOwner {
        require(
            !verifiedHashes[_certificateHash], 
            "Certificate hash already exists"
        );
        
        verifiedHashes[_certificateHash] = true;
        
        emit HashAdded(_certificateHash);
    }
    
    /**
     * @notice Checks if a certificate hash is verified in the registry
     * @param _certificateHash The SHA-256 hash of the certificate to check
     * @return bool True if the certificate hash is verified, false otherwise
     * @dev This is a read-only function that does not modify state
     * @dev Can be called externally without gas consumption
     * 
     * @custom:gas-optimization View function with no gas cost for external calls
     */
    function isVerified(bytes32 _certificateHash) public view returns (bool) {
        return verifiedHashes[_certificateHash];
    }
}
