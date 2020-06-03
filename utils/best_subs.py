
import os
from more_itertools import powerset
import pdb



def best_subset(matchingset, all_flows):
    return_list = [[] for i in all_flows]
    all_length = len(all_flows)
    # print(all_length)

    def _best_subset(matchingset, index):
        nonlocal return_list, all_length
        if len(matchingset) == 1 or index == all_length:
            return len(matchingset)

        maxer = -999
        max_subset = None
        all_subsets = powerset(matchingset)
        all_subsets = list(all_subsets)
        all_subsets.pop(0)
        for s in all_subsets:
            contains_set = False
            # for module-branchsets in experiment
            for f in all_flows[index]:

                if set(s).issubset(f):
                    contains_set = True
                    break

            if not contains_set:
                continue

            best_sub_length = len(s) + _best_subset(s, index + 1)
            if best_sub_length > maxer:
                maxer = best_sub_length
                max_subset = set(s)


        return_list[index].append(max_subset)
        return maxer

    sub = _best_subset(matchingset, 0)


    count =0
    for i in list(return_list):
        tmp = list(set(frozenset(item) for item in i))
        return_list[count] = [set(item) for item in set(frozenset(item) for item in tmp)]
        count+=1
    print(return_list)

    count=0
    new_return_list = [[] for i in all_flows]

    for i in return_list:
        # print(i)
        max_remaining = max(i, key=len)
        new_return_list[count].append(max_remaining)
        max_remaining_prevs_total= set(max_remaining)
        while max_remaining:
            max_remaining = max([set(x-max_remaining_prevs_total) for x in i])
            if len(max_remaining) == 0:
                break
            new_return_list[count].append(max_remaining)
            max_remaining_prevs_total = max_remaining.union(max_remaining_prevs_total)
        count+=1

    # print(new_return_list)
    return new_return_list



a = [[{1,2,6,4,5},{3,7,8},{9}],
    [{1,2,3,4,6},{5,7},{9,8}],
    [{1,2,3,4,5},{7},{4},{6},{8,9}],
    [{1,3,4,5,6,7,8,9},{2}],
    [{1,2},{3,4},{5,6,7},{8,9}]]

b = {1,2,3,4,5,6,7,8,9}


answer = best_subset(b,a)
print(answer)

