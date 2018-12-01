pragma solidity ^0.4.24;

import "./properties/Assignable.sol";
import "./tokens/Likoin.sol";

/**
 * @title Crowdsale
 *
 * @dev Implementation of the base contract for managing a token crowdsale.
 * Originally based on code by OpenZeppelin: https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/crowdsale/Crowdsale.sol
 */
contract Crowdsale is Assignable{
  using SafeMath for uint256;

  // The token being sold
  Likoin private _token;

  // How many token units a buyer gets per wei.
  uint256 private _rate;

  // Amount of wei raised
  uint256 private _weiRaised;

  /**
   * Event for token purchase logging
   */
  event TokensPurchased(address indexed purchaser, address indexed beneficiary, uint256 value, uint256 amount);

  /**
   * @param rate Number of token units a buyer gets per wei
   * @param wallet Address where collected funds will be forwarded to
   * @param token Address of the token being sold
   */
  constructor(uint256 rate, address wallet, Likoin token) public {
    require(rate > 0);
    require(wallet != address(0));
    require(token != address(0));

    _rate = rate;
    _assignee = wallet;
    _token = token;
  }

  /**
   * @dev fallback function
   */
  function () external payable {
    buyTokens(msg.sender);
  }

  /**
   * @dev token purchase
   */
  function buyTokens(address beneficiary) public payable {
    require(beneficiary != address(0));
    uint256 weiAmount = msg.value;
    require(weiAmount != 0);

    // calculate token amount to be created
    uint256 tokens = _getTokenAmount(weiAmount);

    // update state
    _weiRaised = _weiRaised.add(weiAmount);

    _token.mint(beneficiary, tokens);
    emit TokensPurchased(msg.sender, beneficiary, weiAmount, tokens);

    _assignee.transfer(msg.value);
  }

  /**
   * @dev The way in which ether is converted to tokens.
   */
  function _getTokenAmount(uint256 weiAmount) internal view returns (uint256) {
    return weiAmount.mul(_rate);
  }

  /**
   * @return the token being sold.
   */
  function token() public view returns(Likoin) {
    return _token;
  }

  /**
   * @return the number of token units a buyer gets per wei.
   */
  function rate() public view returns(uint256) {
    return _rate;
  }

  /**
   * @return the amount of wei raised.
   */
  function weiRaised() public view returns (uint256) {
    return _weiRaised;
  }
}