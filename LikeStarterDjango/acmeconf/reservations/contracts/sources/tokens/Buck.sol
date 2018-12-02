pragma solidity ^0.4.24;

import "./SimpleToken.sol";

/**
 * @title Buck Token
 */
contract Buck is SimpleToken{

  // Balances
  mapping (address => uint256) _balances;

  // Total supply
  uint256 _totalSpent;

  /**
   * @param assignee Address of the entity token depends on 
   * @param name Token name
   * @param symbol Token symbol
   */
  constructor(address assignee, string name, string symbol) public {
    _owner = msg.sender;
    _assignee = assignee;
    _addMinter(msg.sender);

    _name = name;
    _symbol = symbol;
  }

  /**
  * @dev Consume token for a specified address
  */
  function consume(address account, uint256 value) public onlyMinter returns (bool) {
    _burn(account, value);
    return true;
  }

  /**
   * @dev Internal function that mints an amount of the token and assigns it to
   * an account.
   */
  function _mint(address account, uint256 value) internal {
    require(account != 0);

    _totalSupply = _totalSupply.add(value);
    _balances[account] = _balances[account].add(value);
    emit Transfer(address(0), account, value);
  }

  /**
   * @dev Internal function that burns an amount of the token of a given
   * account.
   */
  function _burn(address account, uint256 value) internal {
    require(account != 0);
    require(value <= _balances[account]);

    _totalSupply = _totalSupply.sub(value);
    _totalSpent = _totalSpent.add(value);
    _balances[account] = _balances[account].sub(value);
    emit Transfer(account, address(0), value);
  }

  /**
  * @dev Total number of tokens spent (burned)
  */
  function totalSpent() public view returns (uint256) {
    return _totalSpent;
  }

  /**
  * @dev Gets the balance of the specified address.
  */
  function balanceOf(address account) public view returns (uint256) {
    return _balances[account];
  }
}