const Likoin = artifacts.require("Likoin.sol");
const Buck = artifacts.require("Buck.sol");
const Voting = artifacts.require("Voting.sol");
const ArtifactsManager = artifacts.require("ArtifactsManager.sol");

contract('Voting', accounts => {
  var owner = accounts[0];
  var alice = accounts[1];
  var bob = accounts[2];
  var carlo = accounts[4];
  var assignee = accounts[3];

  it("should set a new proposal",  async () => {
    const vot = await Voting.deployed();
    const token = await Likoin.deployed();
    const am = await ArtifactsManager.deployed();
    await token.mint(bob, 30000000000000000000, {from: owner});
    await token.mint(alice, 100000000000000000, {from: owner});
    //await token.mint(carlo, 50000000000000000, {from: owner});
    await vot.addArtifactsManager(ArtifactsManager.address, {from: owner});
    await am.proposeArtifact(1, "Compra ora", 5000, {from: assignee});
    bal = await vot.getProposalIdByArtifact(1);
    assert.equal(bal.toNumber(), 0, "Proposal was not correctly set");
  });
  it("should add new suggestion",  async () => {
    const vot = await Voting.deployed();
    const token = await Likoin.deployed();
    await vot.newPriceSuggestion(0, 7000, { from: bob });
    bal = await vot.numberOfProposalSuggestions(0);
    res = await vot.getProposalSuggestionAmount(0, 1);
    assert.equal(bal.toNumber(), 2, "Proposal was not correctly set");
    assert.equal(res.toNumber(), 7000, "Proposal was not correctly set");
  });
  it("should vote",  async () => {
    const vot = await Voting.deployed();
    const token = await Likoin.deployed();
    await vot.vote(0, 1, { from: bob });
    bal = await vot.hasVotedFor(bob, 0, 1);
    assert.equal(bal, true, "Vote was not correct");
  });
  it("should change vote",  async () => {
    const vot = await Voting.deployed();
    const token = await Likoin.deployed();
    await vot.changeVote(0, 0, { from: bob });
    bal1 = await vot.hasVotedFor(bob, 0, 0);
    bal2 = await vot.hasVotedFor(bob, 0, 1);
    assert.equal(bal1, true, "Vote change was not correct");
    assert.equal(bal2, false, "Vote change was not correct");
  });
  it("should execute",  async () => {
    const vot = await Voting.deployed();
    const token = await Likoin.deployed();
    await vot.executeProposal(0, { from: owner });
    bal = await vot.isExecuted(0);
    bal2 = await vot.getProposalFinalResult(0);
    assert.equal(bal, true, "Execute was not correct");
    assert.equal(bal2.toNumber(), 5000, "Vote was not correct");
  });
  it("should add price to artifact",  async () => {
    const am = await ArtifactsManager.deployed();
    bal = await am.isArtifactApproved(1);
    assert.equal(bal, true, "Execute was not correct");
    bal2 = await am.getArtifactPriceByID(1);
    assert.equal(bal2.toNumber(), 5000, "Execute was not correct");
  });
  it("should buy an artifact",  async () => {
    const am = await ArtifactsManager.deployed();
    const buck = await Buck.deployed();
    await buck.addMinter(ArtifactsManager.address, {from: owner});
    await buck.mint(bob, 100000000000000000, {from: owner});
    await am.buyArtifact(1, bob, {from: bob});
    bal = await am.ownership(bob, 1);
    assert.equal(bal, true, "Purchrase was not correct");
  });
});