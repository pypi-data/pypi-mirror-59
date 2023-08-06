# misc.py
#
# This file is part of scqubits.
#
#    Copyright (c) 2019, Jens Koch and Peter Groszkowski
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


import numpy as np


def process_which(which, max_index):
    """
    Parameters
    ----------
    which: int or tuple or list, optional
        single index or tuple/list of integers indexing the eigenobjects.
        If which is -1, all indices up to the max_index limit are included.
    max_index: int
        maximum index value

    Returns
    -------
    list or iterable of indices
    """
    if isinstance(which, int):
        if which == -1:
            return range(max_index)
        return [which]
    return which


def make_bare_labels(hilbertspace, *args):
    """
    For two given subsystem states, return the full-system bare state label obtained by placing all remaining
    subsystems in their ground states.

    Parameters
    ----------
    hilbertspace: HilbertSpace
    *args: tuple(int, int)
        each argument is a tuple of the form (subsys_index, label)

    Returns
    -------
    tuple
        Suppose there are 5 subsystems in total. Let (subsys_index1=0, label1=3), (subsys_index2=2, label2=1). Then the
        returned bare-state tuple is: (3,0,1,0,0)
    """
    bare_labels = [0] * hilbertspace.subsystem_count
    for subsys_index, label in args:
        bare_labels[subsys_index] = label
    return tuple(bare_labels)


def process_metadata(full_dict):
    """Convert an extended system dictionary, as obtained through __dict__, to a reduced one that can be written to
    a file

    Parameters
    ----------
    full_dict: dict
    """
    reduced_dict = {}
    for key, param_obj in full_dict.items():
        if key[0] == '_':
            continue
        if isinstance(param_obj, (int, float, np.number)):
            reduced_dict[key] = param_obj
        elif key == 'grid':
            grid_dict = param_obj._get_metadata_dict()
            reduced_dict.update(grid_dict)
        else:
            reduced_dict[key] = str(param_obj)
    return reduced_dict


def filter_metadata(full_dict):
    """Filter for entries in the full dictionary that have numerical values"""
    reduced_dict = {}
    for param_name, param_value in full_dict.items():
        if isinstance(param_value, (int, float, np.number)):
            reduced_dict[param_name] = param_value
    return reduced_dict
