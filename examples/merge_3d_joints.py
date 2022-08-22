import glob
import os.path as osp
import os
from matplotlib import animation
import matplotlib.pyplot as plt
import json
import numpy as np

def get_data(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
        joints = []
        for joint in data['skeleton']['joints']:
            joints.append((joint['position']['x'], joint['position']['y'], joint['position']['z']))
        return np.array(joints)

import numpy as np
import math

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


fig, axs = plt.subplots(ncols=2, figsize=(10, 5), subplot_kw={"projection": "3d"})
fontlabel = {"fontsize": "large", "color": "gray", "fontweight": "bold"}
data_dir = '' # 수정필요
views = ['master-0', 'sub-1', 'sub-2', 'sub-3', 'sub-4', 'sub-5']

fpath_list = []
for view_nm in views:
    if len(fpath_list) == 0:
        fpath_list = os.listdir(osp.join(data_dir, view_nm))
    else:
        fpath_list_ = os.listdir(osp.join(data_dir, view_nm))
        fpath_list = list(set(fpath_list) & set(fpath_list_))

print(len(fpath_list))
fpath_list = sorted(fpath_list)
print(fpath_list)
