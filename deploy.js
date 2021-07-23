const Landswap = artifacts.require('Landswap');

module.exports = async function (deployer) {
  await deployer.deploy(Landswap);
};