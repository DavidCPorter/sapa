import pip
import sys
import os
import subprocess

def add_branch(branch_list):
    branch_list = branch_list.split(',')

    for i in branch_list:
        output = subprocess.run(['mkdir', i], capture_output=True)
        subprocess.run(['mkdir', i+'/env'])
        subprocess.run(['mkdir', i+'/load'])
        subprocess.run(['mkdir', i+'/pipeline'])
        subprocess.run(['mkdir', i+'/service'])
        subprocess.run(['mkdir', i+'/viz'])


def rm_branch(branch_list):
    branch_list = branch_list.split(',')

    for i in branch_list:
        output = subprocess.run(['mkdir', i], capture_output=True)
        subprocess.run(['mkdir', i+'/env'])
        subprocess.run(['mkdir', i+'/load'])
        subprocess.run(['mkdir', i+'/pipeline'])
        subprocess.run(['mkdir', i+'/service'])
        subprocess.run(['mkdir', i+'/viz'])


def add_module(var_list):
    modules = var_list.split(' ')
    branches = modules.pop()



