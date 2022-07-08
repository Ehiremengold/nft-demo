// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    bytes32 public keyHash;
    uint256 public fee;
    uint256 public randomResult;
    uint256 public tokenCounter;
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }

    mapping(uint256 => string) public tokenIdTotokenURI;
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;
    event requestCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(
        address _vrfCoordinator,
        address _link,
        bytes32 _keyHash,
        uint256 _fee
    ) public VRFConsumerBase(_vrfCoordinator, _link) ERC721("dogiee", "DOG") {
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectable() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        // requestRandomness from the vrf consumber base does
        // the requesting taking the keyhash and fee as parameters
        // check chainlink docs or the github repo for more details
        requestIdToSender[requestId] = msg.sender;
        emit requestCollectible(requestId, msg.sender);
        // uint256 newTokenId = tokenCounter;
        // _safeMint(msg.sender, newTokenId);
        // _setTokenURI(newTokenId, tokenURI);
        // tokenCounter = tokenCounter + 1;
        // return requestId
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Breed breed = Breed(randomNumber % 3);
        // breed = Breed(0,1 or 2)
        // we are going map a token id to each breed
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        address sender = requestIdToSender[requestId];
        _safeMint(sender, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    // Assignment...
    // write a function to set the token uri based
    // on the breed of the dog

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // we are going to need three token URIs
        // "however we want the owner of the token
        // id are able to update the token uri"
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner or approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
