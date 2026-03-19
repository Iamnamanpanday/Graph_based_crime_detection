// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AuditTrail {
    struct FlaggedAccount {
        string accountHash;
        uint256 suspicionScore;
        uint256 timestamp;
    }

    // Mapping of account hash to FlaggedAccount data
    mapping(string => FlaggedAccount) public flaggedAccounts;

    // Event emitted when a new account is logged
    event AccountLogged(string accountHash, uint256 suspicionScore, uint256 timestamp);

    // Function to log a flagged account
    function logAccount(string memory _accountHash, uint256 _suspicionScore) public {
        require(_suspicionScore > 0, "Suspicion score must be greater than 0");

        flaggedAccounts[_accountHash] = FlaggedAccount({
            accountHash: _accountHash,
            suspicionScore: _suspicionScore,
            timestamp: block.timestamp
        });

        emit AccountLogged(_accountHash, _suspicionScore, block.timestamp);
    }

    // Function to retrieve log data for an account hash
    function getLog(string memory _accountHash) public view returns (string memory, uint256, uint256) {
        FlaggedAccount memory acc = flaggedAccounts[_accountHash];
        return (acc.accountHash, acc.suspicionScore, acc.timestamp);
    }
}
