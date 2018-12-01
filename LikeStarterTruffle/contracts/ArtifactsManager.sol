pragma solidity ^0.4.24;

import "./properties/Ownable.sol";
import "./properties/Assignable.sol";
import "./Voting.sol";
import "./tokens/Buck.sol";

/**
 * @title Contract used to manage Artifacts
 */
contract ArtifactsManager is Assignable {

  // The voting contract
  Voting private _voting;

  // The token used for prices
  Buck private _buck;
  
  // List of Artifacts proposed
  mapping (uint => Artifact) private _artifactsProposed;

  // List of Artifacts index
  mapping (uint => uint) private _artifactsIndex;
 
  // Number of Artifacts proposed
  uint private _numArtifactsProposed;

  // Ownership of an artifact by an account 
  mapping (address => mapping (uint => bool)) _ownership; 

  /**
   * Event for an artifact buyed
   */
  event BuyedArtifact(uint artifactID, address purchaser, address beneficiary);

  /**
   * Event for an artifact proposed
   */
  event ProposedArtifact(uint artifactID, string description, uint proposedPrice);

  /**
   * Event for an artifact approved
   */
  event ApprovedArtifact(uint artifactID, uint finalPrice);
  
  /**
   * Structure used to manipulate an artifact
   */
  struct Artifact {
    uint id;
    string description;
    uint price;
    bool approved;
  }

  /**
   * @dev Modifier to allow only the voting contract
   */
  modifier onlyVoting() {
    require(isVoting(msg.sender));
    _;
  }

  /**
   * @param assignee Address of the entity management depends on 
   * @param voting Address of the voting contract
   * @param buck Address of the token used for prices
   */
  constructor (address assignee, Voting voting, Buck buck) public {
    _assignee = assignee;
    _voting = voting;
    _buck = buck;
  }

  /**
   * @dev Buy an artifact using Bucks
   */
  function buyArtifact(uint artifactID, address beneficiary) public returns (bool) {
    require(beneficiary != address(0));
    require (_artifactsIndex[artifactID] >= 0 && _artifactsIndex[artifactID] <= _numArtifactsProposed);
    Artifact storage a = _artifactsProposed[_artifactsIndex[artifactID]];
    require (a.approved);
    require (_buck.balanceOf(msg.sender) >= a.price);
  
      _buck.consume(msg.sender, a.price);
      _ownership[beneficiary][artifactID] = true;
  
      emit BuyedArtifact(artifactID, msg.sender,beneficiary);
  
    return true;    
  }

  /**
   * @dev Propose an artifact to vote
   */
  function proposeArtifact(uint artifactID, string description, uint proposedPrice) public onlyAssignee returns (bool) {
    require(proposedPrice > 0);
    Artifact storage a = _artifactsProposed[_artifactsIndex[artifactID]];
    require (!a.approved);
  
      if(_artifactsIndex[artifactID] >= 0 && _artifactsIndex[artifactID] <= _numArtifactsProposed) {
          a.description = description;
        } else {
          uint arIndex = ++_numArtifactsProposed;
          a = _artifactsProposed[arIndex];
          a.id = artifactID;
          a.description = description;
      }
  
      _voting.newProposal(artifactID, proposedPrice, description);
    
      emit ProposedArtifact(artifactID, description, proposedPrice);
  
    return true;    
  }

  /**
   * @dev Add an artifact after vote
   */
  function approveArtifact(uint artifactID, uint finalPrice) public onlyVoting returns (bool) {
    require (_artifactsIndex[artifactID] >= 0 && _artifactsIndex[artifactID] <= _numArtifactsProposed);
    Artifact storage a = _artifactsProposed[_artifactsIndex[artifactID]];
    require (!a.approved);

    a.approved = true;
    a.price = finalPrice;
  
    emit ApprovedArtifact(artifactID, finalPrice);

    return true;    
  }

  /**
   * @return The voting being used
   */
  function voting() public view returns(Voting) {
    return _voting;
  }

  /**
   * @return The token being used
   */
  function buck() public view returns(Buck) {
    return _buck;
  }

  /**
  * @return Get artifact price by id
  */
  function getArtifactPriceByID(uint artifactID) public view returns (uint) {
    require (_artifactsIndex[artifactID] >= 0 && _artifactsIndex[artifactID] <= _numArtifactsProposed);
    return _artifactsProposed[_artifactsIndex[artifactID]].price;
  }

  /**
  * @return true if the artifact is approved
  */
  function isArtifactApproved(uint artifactID) public view returns (bool) {
    require (_artifactsIndex[artifactID] >= 0 && _artifactsIndex[artifactID] <= _numArtifactsProposed);
    return _artifactsProposed[_artifactsIndex[artifactID]].approved;
  }

  /**
  * @return Number of Artifacts proposed
  */
  function numberOfArtifactsProposed() public view returns (uint) {
    return _numArtifactsProposed;
  }

  /**
  * @return Get artifact id by index
  */
  function getArtifactIDByIndex(uint index) public view returns (uint) {
    require (index >= 0 && index <= _numArtifactsProposed);
    return _artifactsProposed[index].id;
  }

  /**
   * @return true if artifactID is owned by account
   */
  function ownership(address account, uint artifactID) public view returns (bool) {
    return _ownership[account][artifactID];
  }

  /**
   * @dev Function indicating if account is voting contract 
   */
  function isVoting(address account) private view returns (bool) {
    return _voting == account;
  }
}


