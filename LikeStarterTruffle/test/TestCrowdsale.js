const Crowdsale = artifacts.require("Crowdsale.sol");
const Likoin = artifacts.require("Likoin.sol");
const Buck = artifacts.require("Buck.sol");

contract('Crowdsale', accounts => {
  var owner = accounts[0];
  var alice = accounts[1];
  var bob = accounts[2];
  var assignee = accounts[3];

  it("should set Crowdsale as minter",  async () => {
    const crow = await Crowdsale.deployed();
    const token = await Likoin.deployed();
    await token.addMinter(Crowdsale.address);
    min = await token.isMinter(Crowdsale.address);
    assert.equal(min, true, "Minter was not correctly set");
  });
  it("should buy tokens",  async () => {
    const crow = await Crowdsale.deployed();
    const token = await Likoin.deployed();
    await crow.buyTokens(bob, { from: bob, value: 10000 });
    await crow.buyTokens(alice, { from: bob, value: 10000 });
    bal = await token.balanceOf(bob);
    rate = await crow.rate();
    assert.equal(bal.toNumber(), 10000 * rate, "Tokens were not correctly buyed");
  });
  it("should convert tokens",  async () => {
    const crow = await Crowdsale.deployed();
    const token = await Likoin.deployed();
    const buck = await Buck.deployed();
    await buck.addMinter(Likoin.address);
    crate = await token.conversionRate();
    await token.convertToBucks(100, { from: bob });
    balb = await buck.balanceOf(bob);
    assert.equal(balb.toNumber(), 100 * crate, "Tokens were not correctly converted");
  });
});
