pragma solidity ^0.4.24;

import "./SimpleToken.sol";
import "./Buck.sol";

/**
 * @title ERC20 token
 *
 * @dev Implementation of the basic standard token.
 * https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md
 * Originally based on code by OpenZeppelin: https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/token/ERC20/ERC20.sol
 */
contract Likoin is SimpleToken{

  // the token being converted to
  Buck private _buck;

  // How many bucks a buyer gets per token.
  uint256 private _conversionRate;

  // Balances
  mapping (address => uint256[2]) _balances;

  // Allowances mapping, used to allow an address to spend another address tokens 
  mapping (address => mapping (address => uint256)) private _allowed;
  
  // Addresses of holders, list that starts from 1
  mapping (uint256 => address) private _balanceHolders;

  // Index of last holder in list
  uint256 _holdersIndex;

  /**
   * Event for token conversion
   */
  event TokensConversion(address indexed beneficiary, uint256 amount);

  /**
   * Event for an approval
   */
  event Approval( address indexed owner, address indexed spender, uint256 value);


  /**
   * @param assignee Address of the entity token depends on 
   * @param buck Address of the token used for conversion
   * @param conversionRate Number of buck units a buyer gets per tokens
   * @param name Token name
   * @param symbol Token symbol
   */
  constructor(address assignee, Buck buck, uint256 conversionRate, string name, string symbol) public {
    require(conversionRate > 0);
    require(assignee != address(0));
    require(buck != address(0));

    _owner = msg.sender;
    _assignee = assignee;
    _addMinter(msg.sender);
    _addMinter(assignee);

    _name = name;
    _symbol = symbol;
    _buck = buck;
    _conversionRate = conversionRate;
  }

  /**
  * @dev Transfer token to a specified address
  */
  function transfer(address to, uint256 value) public returns (bool) {
    _transfer(msg.sender, to, value);
    return true;
  }

  /**
   * @dev The way in which tokens are converted to bucks.
   */
  function convertToBucks(uint256 value) public returns (bool success) {
    require(balanceOf(msg.sender) >= value);

    _shareToken(msg.sender, value);

    emit TokensConversion(msg.sender, value); 

    uint256 bucks = value * _conversionRate;
    _buck.mint(msg.sender, bucks);

    return true;
  }

  /**
   * @dev Approve the passed address to spend the specified amount of tokens on behalf of msg.sender.
   */
  function approve(address spender, uint256 value) public returns (bool) {
    require(spender != address(0));

    _allowed[msg.sender][spender] = value;
    emit Approval(msg.sender, spender, value);
    return true;
  }

  /**
   * @dev Transfer tokens from one address to another if the address from approved msg.sender
   */
  function transferFrom(address from, address to, uint256 value) public returns (bool) {
    require(value <= _allowed[from][msg.sender]);

    _allowed[from][msg.sender] = _allowed[from][msg.sender].sub(value);
    _transfer(from, to, value);
    return true;
  }

  /**
   * @dev Increase the amount of tokens that an owner allowed to a spender.
   */
  function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
    require(spender != address(0));

    _allowed[msg.sender][spender] = (_allowed[msg.sender][spender].add(addedValue));
    emit Approval(msg.sender, spender, _allowed[msg.sender][spender]);
    return true;
  }

  /**
   * @dev Decrease the amount of tokens that an owner allowed to a spender.
   */
  function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
    require(spender != address(0));

    _allowed[msg.sender][spender] = (
      _allowed[msg.sender][spender].sub(subtractedValue));
    emit Approval(msg.sender, spender, _allowed[msg.sender][spender]);
    return true;
  }

  /**
  * @dev Transfer token for a specified addresses
  */
  function _transfer(address from, address to, uint256 value) internal {
    require(value <= _balances[from][0]);
    require(to != address(0));

    if(_balances[to][0] <= 0){
        _addHolder(to);
    }

    _balances[from][0] = _balances[from][0].sub(value);
    _balances[to][0] = _balances[to][0].add(value);

    if(_balances[from][0] <= 0){
        _removeHolder(from);
    }
    emit Transfer(from, to, value);
  }

  /**
   * @dev Internal function that mints an amount of the token and assigns it to
   * an account.
   */
  function _mint(address account, uint256 value) internal {
    require(account != 0);
    if(_balances[account][0] <= 0){
        _addHolder(account);
    }

    _totalSupply = _totalSupply.add(value);
    _balances[account][0] = _balances[account][0].add(value);
    emit Transfer(address(0), account, value);
  }

  /**
   * @dev Share value tokens between all addresses except from 
   */
  function _shareToken(address from, uint256 value) internal returns (bool) {
    
    for(uint i = 1; i <= _holdersIndex; i++){
      if(to != from){
        address to = _balanceHolders[i];
        uint256 bal = balanceOf(to); 
        _transfer(from, to, value.mul(bal.div(_totalSupply.sub(value))));
        //value * ( balance[to] / (totalSupply-value) )
      }
    }

    return true;
  }

  /**
   * @dev Internal function that burns an amount of the token of a given
   * account.
   */
  function _burn(address account, uint256 value) internal {
    require(account != 0);
    require(value <= _balances[account][0]);

    _totalSupply = _totalSupply.sub(value);
    _balances[account][0] = _balances[account][0].sub(value);
    emit Transfer(account, address(0), value);
  }

  /**
   * @dev Internal function that burns an amount of the token of a given
   * account, deducting from the sender's allowance for said account.
   */
  function _burnFrom(address account, uint256 value) internal {
    require(value <= _allowed[account][msg.sender]);

    _allowed[account][msg.sender] = _allowed[account][msg.sender].sub(
      value);
    _burn(account, value);
    if(_balances[account][0] <= 0){
        _removeHolder(account);
    }
  }

  /**
   * @dev Internal function that adds an holder
   */
  function _addHolder(address account) internal {
    _balanceHolders[++_holdersIndex] = account;
    _balances[account][1] = _holdersIndex;
  }

  /**
   * @dev Internal function that removes an holder
   */
  function _removeHolder(address account) internal {
    uint256 index = _balances[account][1];
    if (index < 1) return;

    if(_holdersIndex > 1){
      address last = _balanceHolders[_holdersIndex];
      _balanceHolders[index] = last;
      _balances[last][1] = index;
    }
    _holdersIndex--;
    
    _balances[account][1] = 0;
  }

  /**
   * @return the token being used for conversion.
   */
  function buck() public view returns(Buck) {
    return _buck;
  }

  /**
   * @return the number of buck units a buyer gets per token.
   */
  function conversionRate() public view returns(uint256) {
    return _conversionRate;
  }

  /**
  * @dev Gets the balance of the specified address.
  */
  function balanceOf(address account) public view returns (uint256) {
    return _balances[account][0];
  }

  /**
   * @dev Function to check the amount of tokens that an owner allowed to a spender.
   */
  function allowance(address owner, address spender) public view returns (uint256) {
    return _allowed[owner][spender];
  }

  /**
   * @dev Function that returns the balanceHolders length 
   */
  function getBalanceHoldersLength() public view returns (uint256) {
    return _holdersIndex;
  }

  /**
   * @dev Function that returns the address in position i of balanceHolders
   */
  function getBalanceHolder(uint256 i) public view returns (address) {
    require (i <= _holdersIndex);
    
    return _balanceHolders[i];
  }
}