import pdb
import traceback

import pip
import sys
import os
import subprocess
import janusutils as janusUtils
import _ssh_import as ssh_import
from _branch_class import Experiment
from typing import Set
from itertools import permutations

import yaml
from collections import OrderedDict
from jinja2 import Template
import re
from _graph_node import Noder


# pass in all active branch names
def update_groupnames(branch_names: Set):
    groupnames_list = []
    valid_groupnames_dict = {}
    for r in range(1, len(branch_names)+1):
        itertools = permutations(branch_names, r)
        for i in itertools:
            groupnames_list.append(','.join(i))
            valid_groupnames_dict.update({','.join(i) : set(i)})


    for i in groupnames_list:
        set_to_remove = set(i.split(','))
        value_set = branch_names - set_to_remove
        valid_groupnames_dict.update({'all!'+i : value_set})

    valid_groupnames_dict.update({'all' : branch_names})

    return valid_groupnames_dict



def commandDispatcher(exp_dict):
    name = exp_dict.get('--name')
    home_dir = exp_dict.get('--home')
    r_modules = home_dir + '/jmods'
    stages = {'env', 'load', 'pipeline', 'service', 'viz'}
    available_modules = {x : list() for x in stages}


    for stage in os.scandir(r_modules):
        if stage.name in stages:
            available_modules.update({stage.name: [x.name for x in os.scandir(stage.path)]})
    allmods = available_modules.values()
    module_play_order = {mod : OrderedDict() for m_list in allmods for mod in m_list}
    module_var_order= {mod : OrderedDict() for m_list in allmods for mod in m_list}
    for stage in os.scandir(r_modules):
        if stage.name in stages:
            for m in os.scandir(r_modules+'/'+stage.name):
                play_list = []
                for j in os.scandir(r_modules+'/'+stage.name+'/'+m.name+'/'+'plays'):
                   play_list.append(j.name)
                play_list.sort()
                variable_pos = 1
                for pname in play_list:
                    pname_path = r_modules+'/'+stage.name+'/'+m.name+'/'+'plays/'+pname
                    # update dict in order
                    # implies the play directiory is listed in order
                    play_dict = module_play_order.get(m.name)
                    play_dict.update({pname: 'all'})
                    module_play_order.update({m.name: play_dict})
                    ordered_var_dict = module_var_order.get(m.name)

                    rgx = re.compile('{{(?P<name>[^{}]+)}}')
                    #  open play file and read the variabels in order to pass as a control dict to Experiment cls
                    with open(r_modules+'/'+stage.name+'/'+m.name+'/'+'plays/'+pname, 'r') as playfile:
                        for line in playfile.readlines():
                            if '{{' not in line:
                                continue
                            tmpl = Template(line)
                            var_keys = {match.group('name') for match in rgx.finditer(line)}

                            for v in var_keys:
                                if v not in ordered_var_dict:
                                    ordered_var_dict.update({v:(variable_pos,pname)})
                                    variable_pos+=1

                    # print(m.name)

    tmp = set()
    try:

        for branch in os.scandir('.'):
            if branch.is_dir():
                tmp.add(branch.name)

        # create a hostfile that ~/.ssh/config includes temporarily that treats branches as a host so you can apply var updates to them all... just my preferred way to keep tabs on all var updates for the exp.
        ssh_import.new_branch(tmp, exp_dict.get('--home_user'), home_dir)

        # make local_var_inventory file for vars
        ssh_import.new_inventory(tmp, exp_dict.get('--home_user'))



    except (RuntimeError, TypeError, NameError) as e:
        print(e)
        return 1

    # experiment_modules
    experiment = Experiment(name, available_modules, r_modules, module_play_order, module_var_order, [b_name for b_name in tmp])

    # this dict maps ansible groupname notation to a set of branch_names
    valid_groupnames_dict = update_groupnames(tmp)

    # for i in valid_groupnames_dict.keys():
    #     print(f'{i} --> {valid_groupnames_dict.get(i)}')

    # this is experimental context used to pass commands to in the user input loop in main
    def cmdFetcher(args):
        nonlocal valid_groupnames_dict

        if args[-1] not in valid_groupnames_dict.keys():
            groups = 'all'

        else:
            groups = args.pop()

        target_branch_set = valid_groupnames_dict.get(groups)

        def ls(vars,target_branches):
            nonlocal experiment


            if vars[0] == 'modules':
                print('yes')
                experiment.show_ordered_mods(target_branches)

            if vars[0] == 'vars':
                cli_options = vars[1:]
                cli_options_dict = {cli_options[x]: cli_options[x + 1] for x in range(0, len(cli_options) - 1) if
                                    x % 2 == 0}
                experiment.ls('vars', cli_options_dict, target_branches)

            #
            if vars[0] == 'branches':
                print(experiment.branches)

        def load(vars, target_branches):

            filename = vars.pop()
            cmd_list = [line.rstrip() for line in open(filename)]
            return_list = []
            for cmd in cmd_list:
                return_list.append(cmd.split(' '))

            return return_list


        def add(vars,target_branches):
            if len(vars) < 2:
                print(f'vars {vars} incorrect')
                return

            nonlocal experiment,valid_groupnames_dict

            if vars[0] == 'branch':
                experiment.add_branch(vars[1])
                branch_names = set(experiment.branches.keys())
                valid_groupnames_dict = update_groupnames(branch_names.union(target_branches))
                print('success')

            elif vars[0] == 'modules' or vars[0] == 'module':
                experiment.update_modules('add', vars[1:], target_branches)

            elif vars[0] == 'vars':
                user_variables = vars[1:]
                experiment.update_variables(user_variables, target_branches)


            elif vars[0] == 'hosts':
                if len(vars) < 4:
                    print(f'\nJANUS assumes you left out playname(s) argument, so default behavior applied changes to all plays')
                    vars.append('all')
                hostgroup = vars[1]
                modulename = vars[2]
                playname = vars[3]
                experiment.update_hostgroups(hostgroup, modulename, playname, target_branches)

        def rm(vars,target_branches):
            nonlocal experiment, valid_groupnames_dict
            if vars[0] == 'branch' or vars[0] == 'branches':
                experiment.rm_branches(target_branches)
                valid_groupnames_dict = update_groupnames(set(experiment.branches.keys()))
                print(f'\n\nsuccess')

            if vars[0] == 'modules' or vars[0] == 'module':
                experiment.update_modules('rm', vars[1].split(','), target_branches)

        def show(vars, target_branches):
            if vars[0] == 'tree':
                branch_order = experiment.get_branch_flow_order([b for b in experiment.branches.values()], list_flag='filtered')
                print(branch_order)
                return
            if vars[0] == 'order':
                start_args = ['show', 'modules']
                start(start_args, target_branches)
                return

            if vars[0] == 'vars':
                start_args = ['flag', 'vars']
                start(start_args, target_branches)
                return


        # janus cmd does project operations when in interactive mode
        def janus(vars,target_branches):
            nonlocal experiment
            if vars[0] == 'add' and vars[1] == 'branch':
                add(vars[1:], target_branches)
            elif vars[0] == 'ls' and vars[1] == 'branches':
                ls(vars[1:], target_branches)

            else:
                print(f'\n\njanus command did not match operation')

        # offers "module" order support.
        def order(vars,target_branches):
            nonlocal experiment
            ordered_list = vars[1:]
            experiment.update_modules('order', ordered_list, target_branches)

        def start(vars, target_branches):
            nonlocal experiment
            params_dict = {vars[x]: vars[x + 1] for x in range(0, len(vars) - 1) if x % 2 == 0}
            # returns a list of lists of sets each set in a list represents a single branch, and each list in a list is a different point in the module order.
            raw_branching_order = experiment.get_branch_flow_order([b for b in experiment.branches.values()], list_flag='unfiltered')
            print('raw_branching_order')
            print(raw_branching_order)
            optimal_branching_order = experiment.get_branch_flow_order([b for b in experiment.branches.values()], list_flag='filtered')
            print(f'\n\n optimal_branch_order')
            print(optimal_branching_order)
            final_list = list()

            # make a graph out of the optimal branch order
            def explore_next(node):
                nonlocal final_list
                if node.neighbors == None:
                    final_list.append(node.value)
                    return
                union_set = set()
                for i in node.neighbors:
                    if i.value.issubset(node.value):
                        union_set = union_set.union(i.value)
                        explore_next(i)
                if len(node.value - union_set) > 0:
                    final_list.append(node.value-union_set)

            # Creates Nodes representation of optimal branchorder
            graph = [[Noder(set(i),None) for i in j] for j in optimal_branching_order ]
            rootNode = Noder({t for t in target_branches}, graph[0])
            next_level=0
            for i in graph:
                next_level+=1
                if next_level == len(graph):
                    break
                for j in i:
                    # set reference to neighbors
                    j.neighbors = graph[next_level]


            explore_next(rootNode)
            print(f'\n\nfinal_list')
            print(final_list)
            # list of branches with each branch represented by set of unique var tuples
            set_of_diff_vars_per_branch = experiment.get_vars_to_branch_on(final_list, raw_branching_order)
            print(f'\n\n sets of diff vars per branch')
            print(set_of_diff_vars_per_branch)

            # returns list of list tuples(branch_name, module, play_to_start_from)
            ordered_sets_of_branches = experiment.order_branches_by_var_precedence(set_of_diff_vars_per_branch, final_list)
            print(f'\n\nordered_sets of branches')
            print(ordered_sets_of_branches)

            final_schedule = experiment.get_schedule(ordered_sets_of_branches, raw_branching_order)
            # pdb.set_trace()
            print(f'\n\nfinal schedule')
            print(final_schedule)
            # this would be called by show modules
            if params_dict.get('show') == 'modules':
                pref = 1
                print(f'\n\nbranch_name  |  branch_on_module  |  branch_on_play\n ')
                for b in final_schedule:
                    print(f' {pref}) {b[0]}  |  {b[1]}  |  {b[3]}')
                    pref+=1
                return

            if params_dict.get('show') == 'vars':
                print(f'\n\n collecting runtime variables \n\n')
                shotgun, first_branch, mod_start, play_start = experiment.prepare_experiment(final_schedule, 'vars')
                print(first_branch, mod_start, play_start)
                shotgun(first_branch, mod_start, play_start, global_update_flag=True)
                return
            # walk the branches connected
            ex_flag = None
            if params_dict.get('flag'):
                ex_flag = params_dict.get('flag')

            shotgun,first_branch,mod_start,play_start = experiment.prepare_experiment(final_schedule, ex_flag)
            print(first_branch,mod_start,play_start)
            shotgun(first_branch,mod_start,play_start)

            return


        decorated_command = dict(add=add, rm=rm, ls=ls, janus=janus, order=order, show=show, start=start, load=load)

        return_function = decorated_command.get(args[0])

        # if command was 'ls [group]' or 'ls' then default to vars
        if len(args) == 1 and args[0] == 'ls':
            args.append('vars')

        # remove command from args to return function
        args = args[1:]

        return return_function, args, target_branch_set

    return cmdFetcher


def main(interactive_dict):
    print(interactive_dict)
    os.chdir(str(interactive_dict.get('--home')) + '/experiments/' + str(interactive_dict.get('--name')))

    experiment_context = commandDispatcher(interactive_dict)
    user_command = ''

    while user_command != 'exit':
        user_command = input('> ')
        user_command.split()
        user_command.replace('  ', ' ')

        if user_command == '' or user_command == 'exit':
            # print('continue')
            continue

        user_command_list = user_command.split(' ')
        if user_command_list[-1] == '':
            user_command_list.pop()
        try:
            load_commands = [list(user_command_list)]
            while load_commands:
                cmd,args,target_branches = experiment_context(load_commands.pop(0))
                if cmd:
                    load_response = cmd(args,target_branches)
                    if load_response:
                        load_commands = list(load_response)
                else:
                    print('command not found')
                    break

        except (RuntimeError, TypeError, NameError, IndexError) as e:
            traceback.print_exc()
            print("error -> ", e)



if __name__ == '__main__':
    print(sys.argv)
    args = sys.argv[1:]
    i_dict = {args[x]: args[x + 1] for x in range(0, len(args) - 1) if x % 2 == 0}
    main(i_dict)
    sys.exit()
