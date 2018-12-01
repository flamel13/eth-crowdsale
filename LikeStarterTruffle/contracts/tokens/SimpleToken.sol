pragma solidity ^0.4.24;

import "../properties/Mintable.sol";
import "../properties/Assignable.sol";
import "../utils/SafeMath.sol";

/**
 * @title Simple token
 */
contract SimpleToken is Mintable, Assignable {
  using SafeMath for uint256;

  // Token name 
  string _name;

  // Token symbol
  string _symbol;

  // Decimal places  
  uint8 constant _decimals = 18; 

  // Total supply
  uint256 _totalSupply;

  /**
   * Event for token transfer
   */
  event Transfer(address indexed from, address indexed to, uint256 value);

  /**
  * @dev Name of token
  */
  function name() public view returns (string) {
    return _name;
  }

  /**
  * @dev Symbol of token
  */
  function symbol() public view returns (string) {
    return _symbol;
  }

  /**
  * @dev Decimals of token
  */
  function decimals() public view returns (uint8) {
    return _decimals;
  }

  /**
  * @dev Total number of tokens in existence
  */
  function totalSupply() public view returns (uint256) {
    return _totalSupply;
  }

}