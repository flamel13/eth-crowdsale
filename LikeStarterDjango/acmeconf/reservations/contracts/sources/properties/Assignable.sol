pragma solidity ^0.4.24;

/**
 * @title Assignable contract
 */
contract Assignable {

  // Entity contract depends on 
  address _assignee;

  /**
   * @dev Modifier to allow only the assignee
   */
  modifier onlyAssignee() {
    require(isAssignee(msg.sender));
    _;
  }

  /**
  * @return Assignee 
  */
  function assignee() public view returns (address) {
    return _assignee;
  }

  /**
   * @dev Function indicating if account is assignee 
   */
  function isAssignee(address account) public view returns (bool) {
    return _assignee == account;
  }

}