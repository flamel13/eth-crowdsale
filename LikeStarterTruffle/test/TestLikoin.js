const Likoin = artifacts.require("Likoin.sol");

contract('Likoin', accounts => {
  var owner = accounts[0];
  var alice = accounts[1];
  var bob = accounts[2];
  var assignee = accounts[3];

  it("should mint accounts[2]",  async () => {
  	const token = await Likoin.deployed();
    response = await token.mint.call(bob, 300, { from: owner });
    assert.equal(response, true, "No minted");
  });
  it('should mint bob', async () => {
    const token = await Likoin.deployed();
    await token.mint(bob, 300, { from: owner });
    await token.mint(alice, 300, { from: assignee });
    bal = await token.balanceOf(bob);
    aal = await token.balanceOf(alice);
    assert.equal(bal.toNumber(), 300, "Amount was not correctly minted");
    assert.equal(aal.toNumber(), 300, "Amount was not correctly minted");
  });
  /*Works 
  it('should not mint anyone', async () => {
    const token = await Likoin.deployed();
    await token.mint(bob, 300, { from: bob });
    await token.mint(alice, 300, { from: bob });
    bal = await token.balanceOf(bob);
    aal = await token.balanceOf(alice);
    assert.equal(bal.toNumber(), 0, "Amount was not correctly minted");
    assert.equal(aal.toNumber(), 0, "Amount was not correctly minted");
  });*/
  it('should transfer 300 from bob to alice', async () => {
    const token = await Likoin.deployed();
    await token.transfer(alice, 300, { from: bob });
    bal = await token.balanceOf(bob);
    aal = await token.balanceOf(alice);
    assert.equal(bal.toNumber(), 0, "Amount was not correctly transferred");
    assert.equal(aal.toNumber(), 600, "Amount was not correctly transferred");
  });
  it('should get last balanceholder', async () => {
    const token = await Likoin.deployed();
    response = await token.getBalanceHoldersLength({ from: bob });
    resp = await token.getBalanceHolder(response.toNumber());
    assert.equal(response.toNumber(), 1, "Bob was not deleted");
    assert.equal(resp, alice, "Deletion error");
  });

});
