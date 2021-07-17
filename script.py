import json
import os
import sys
import subprocess


#-------------------------------------------------------------------------------
token_name = ''
token_symbol = ''
directory_slash = '/'
tokens = 'tokens'
root_dir = ''
token_dir = ''

hardhat_config = '''
    /**
    * @type import('hardhat/config').HardhatUserConfig
    */
    require('@nomiclabs/hardhat-ethers');


    module.exports = {
        solidity: "0.8.4",
    };'''

sol_content = ''

#-------------------------------------------------------------------------------
def write_file(file_name, new_content):
    with open(file_name,'r+') as f:
        old_content = f.readlines()
        f.seek(0)
        f.write(new_content)
        if len(old_content) > len(new_content):
            pass
        f.truncate()

def generate_token_code(token_name, token_symbol):
    root_dir = os.getcwd()

    #create new folder for new token
    token_dir = root_dir + directory_slash + tokens + directory_slash + token_name
    os.mkdir(token_dir)
    os.chdir(token_dir)

    subprocess.run('npm init -y', shell=True, check=True)
    subprocess.run('npm install --save-dev hardhat', shell=True, check=True)
    subprocess.run('npm install --save-dev @nomiclabs/hardhat-ethers ethers', shell=True, check=True)
    
    hardhat_config_file = token_dir + directory_slash + 'hardhat.config.js'
    try:
        f = open(hardhat_config_file, 'r')
    except IOError:
        f = open(hardhat_config_file, 'w')
    write_file(hardhat_config_file, hardhat_config)

    subprocess.run('npm install @openzeppelin/contracts', shell=True, check=True)

    #create new folder for new token
    contracts_dir = token_dir + directory_slash + 'contracts'
    os.mkdir(contracts_dir)
    os.chdir(contracts_dir)
    #create sol file
    sol_file = contracts_dir + directory_slash + token_name + '.sol'
    try:
        f = open(sol_file, 'r')
    except IOError:
        f = open(sol_file, 'w')

    #format sol file with params
    sol_content ='''
    pragma solidity ^0.8.0;
    import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

    contract Landswap is ERC20 {{
        constructor() ERC20('{token_name}', '{token_symbol}') 
        {{ }}
    }}'''
    sol_content = sol_content.format(token_name=token_name, token_symbol=token_symbol)
    sol_content = sol_content.replace('{{', '{')
    sol_content = sol_content.replace('}}', '}')
    write_file(sol_file, sol_content)
    
    subprocess.run('npx hardhat compile', shell=True, check=True)

#-------------------------------------------------------------------------------
def main(argv):
    try:
        if (len(argv) == 2 and len(str(argv[1])) < 4):
            #check if argv[0] & argv[1] in countries tuples
            token_name, token_symbol = argv
            #main function
            generate_token_code(token_name, token_symbol)
    except Exception as e:
        print(e)

    pass
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    #token_name = 'Landswap'
    #token_symbol = 'LST'
    main(sys.argv[1:])

    #TODO deployment either with hardhat or change to truffle
