const Likoin = artifacts.require('./tokens/Likoin.sol');
const Buck = artifacts.require('./tokens/Buck.sol');
const Crowdsale = artifacts.require('./Crowdsale.sol');
const Voting = artifacts.require('./Voting.sol');
const ArtifactsManager = artifacts.require('./ArtifactsManager.sol');

module.exports = function(deployer, network, accounts) {
    const rate = new web3.BigNumber(1000);
    const conversionRate = new web3.BigNumber(100);
    const assignee = accounts[3];

    return deployer
        .then(() => {
            return deployer.deploy(
                Buck,
                assignee,
                "Buck1",
                "BK1"
            );
        })
        .then(() => {
            return deployer.deploy(
                Likoin,
                assignee,
                Buck.address,
                conversionRate,
                "Like1",
                "LK1"
            );
        })
        .then(() => {
            return deployer.deploy(
                Crowdsale,
                rate,
                assignee,
                Likoin.address
            );
        })
        .then(() => {
            return deployer.deploy(
                Voting,
                Likoin.address,
                1,
                0
            );
        })
        .then(() => {
            return deployer.deploy(
                ArtifactsManager,
                assignee,
                Voting.address,
                Buck.address
            );
        });
};

/*
const Likoin = artifacts.require('./Likoin.sol');
const Buck = artifacts.require('./Buck.sol');
const Crowdsale = artifacts.require('./Crowdsale.sol');

module.exports = async(deployer, accounts) => {
    const rate = new web3.BigNumber(1000);
    const assignee = accounts[3];

    const token = await Likoin.deployed();
    const buck = await Buck.deployed();
    let response = await deployer.deploy(
                Crowdsale,
                rate,
                assignee,
                Likoin.address,
                Buck.address
            );
}; */