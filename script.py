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

#-------------------------------------------------------------------------------
def init_truffle():

    try:
        os.mkdir(token_dir)
    except:
        print('Token directory already exists.',token_dir)
    os.chdir(token_dir)

    #node and truffle init
    try:
        subprocess.run('npm init -y', shell=True, check=True)
        subprocess.run('npm install --save-dev truffle', shell=True, check=True)
        subprocess.run('npm audit fix --force', shell=True, check=True)
        
        #test network for deployment
        subprocess.run('npm install --save-dev ganache-cli', shell=True, check=True)
    except:
        print('Truffle init failed.')

#-------------------------------------------------------------------------------
def config_creation():

    truffle_config_setup = root_dir + directory_slash + 'truffle-config.js'
    truffle_config_file = token_dir + directory_slash + 'truffle-config.js'
    subprocess.run('npm install --save-dev @openzeppelin/contracts', shell=True, check=True)
    config_list = []
    config_content = ''
    try:
        f_config = open(truffle_config_setup, 'r')
        f_config.seek(0)
        config_list = f_config.readlines()
    except IOError:
        print('No truffle config setup file found.')

    try:
        f = open(truffle_config_file, 'r')
    except IOError:
        f = open(truffle_config_file, 'w')
    f_config.close()
    f.close()

    for el in config_list:
        config_content += el

    write_file(truffle_config_file, config_content)

#-------------------------------------------------------------------------------
def sol_creation():

    contracts_dir = token_dir + directory_slash + 'contracts'
    os.mkdir(contracts_dir)
    os.chdir(contracts_dir)

    #create sol file
    sol_file = contracts_dir + directory_slash + token_name + '.sol'

    sol_template = root_dir + directory_slash + 'Template.sol'
    sol_content_list = []
    sol_content = ''
    try:
        f_template = open(sol_template, 'r')
        f_template.seek(0)
        sol_content_list = f_template.readlines()
    except IOError:
        print('No template.sol file found.')
    #format and write sol file with params
    try:
        f = open(sol_file, 'r')
    except IOError:
        f = open(sol_file, 'w')

    f_template.close()
    f.close()
    for el in sol_content_list:
        sol_content += el
    sol_content = sol_content.format(token_name=token_name, token_symbol=token_symbol)
    sol_content = sol_content.replace('{{', '{')
    sol_content = sol_content.replace('}}', '}')
    write_file(sol_file, sol_content)

#-------------------------------------------------------------------------------
def generate_token_code(token_name, token_symbol):
    global root_dir 
    root_dir = os.getcwd()

    #create new folder for new token
    global token_dir 
    token_dir = root_dir + directory_slash + tokens + directory_slash + token_name
    init_truffle()

    #create a new truffle-config.js for new token
    config_creation()

    #create new folder for new token
    sol_creation()
    
    #compile with truffle
    subprocess.run('npx truffle compile', shell=True, check=True)


#-------------------------------------------------------------------------------
def deploy_creation():

    deploy_config = root_dir + directory_slash + 'deploy.js'
    deploy_file = token_dir + directory_slash + 'deploy.js'
    subprocess.run('npx ganache-cli --deterministic', shell=True, check=True)
    deploy_list = []
    deploy_content = ''
    try:
        f_config = open(deploy_config, 'r')
        f_config.seek(0)
        deploy_list = f_config.readlines()
    except IOError:
        print('No truffle config setup file found.')

    try:
        f = open(deploy_file, 'r')
    except IOError:
        f = open(deploy_file, 'w')
    f_config.close()
    f.close()

    for el in deploy_list:
        deploy_content += el

    write_file(deploy_file, deploy_content)

#-------------------------------------------------------------------------------
def init_deploy():

    #migrations dir 
    migrations_dir = token_dir + directory_slash + 'migrations'
    os.mkdir(migrations_dir)
    os.chdir(migrations_dir)

#-------------------------------------------------------------------------------
def deploy_token():
    #https://docs.openzeppelin.com/learn/deploying-and-interacting
    init_deploy()
    deploy_creation()

    subprocess.run('npx truffle migrate --network development', shell=True, check=True)

#-------------------------------------------------------------------------------
def main(argv):
    try:
        if (len(argv) == 2 and len(str(argv[1])) < 4):
            #check if argv[0] & argv[1] in countries tuples
            token_name, token_symbol = argv
            #main function
            generate_token_code(token_name, token_symbol)
            deploy_token()
    except Exception:
        print('Wrong usage.')
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    #token_name = 'Landswap'
    #token_symbol = 'LST'
    main(sys.argv[1:])
