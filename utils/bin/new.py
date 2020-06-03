import pip
import sys
import os
import subprocess
from yaml import safe_load, safe_dump
from shutil import copyfile

def main(args):
    print(args)
    arg_dict = {args[x]: args[x + 1] for x in range(0, len(args) - 1) if x % 2 == 0}
    branch_list=arg_dict.get("--branches")
    exp_name=arg_dict.get("--name")
    home=arg_dict.get("--home")
    branch_list = branch_list.split(',')
    output = subprocess.run(['mkdir', home + '/experiments/' + exp_name ], capture_output=True)


    for i in branch_list:
        output = subprocess.run(['mkdir', home+'/experiments/'+exp_name+'/'+i], capture_output=True)
        # open(home+'/experiments/'+exp_name+'/inventory', )
        # could add multi-inventory mode here, for now it's a single inv for all branches.
        copyfile(home+'/utils/inventory', home+'/experiments/'+exp_name+'/inventory')
        copyfile(home+'/utils/janusfile', home+'/experiments/'+exp_name+'/janusfile')
        subprocess.run(['mkdir', home+'/experiments/'+exp_name+'/'+i+'/env'])
        subprocess.run(['mkdir', home+'/experiments/'+exp_name+'/'+i+'/load'])
        subprocess.run(['mkdir', home+'/experiments/'+exp_name+'/'+i+'/pipeline'])
        subprocess.run(['mkdir', home+'/experiments/'+exp_name+'/'+i+'/service'])
        subprocess.run(['mkdir', home+'/experiments/'+exp_name+'/'+i+'/viz'])
        with open(home+'/experiments/'+exp_name+'/'+i+'/mod_order.yml', 'w+') as f:
            safe_dump({'module_order': None}, f)
        open(home+'/experiments/'+exp_name+'/'+i+'/user_variables.yml', 'a').close()
        open(home + '/experiments/' + exp_name + '/' + i + '/branch_globals.yml', 'a').close()

if __name__ == '__main__':
    # print (sys.argv)
    main(sys.argv[2:])
    sys.exit()

