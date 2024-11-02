"""Create vector addition app."""
import argparse
import os
import shutil

import vitis

# settings
top_dir = os.path.dirname(os.path.abspath(__file__))
ws_dir = os.path.join(top_dir, '_vitis-ws')
pfm_dir = os.path.join(top_dir, '_pfm')

# check input
assert os.path.exists(pfm_dir)

if os.path.exists(ws_dir):
    print('[INFO] removing existing workspace...')
    shutil.rmtree(ws_dir) 

# start building
client = vitis.create_client()

status = client.set_workspace(path=ws_dir)
assert (status)
status = client.add_platform_repos(platform=os.path.join(pfm_dir, 'kv260', 'export', 'kv260'))
assert (status)
proj = client.create_sys_project(
    name='vadd',
    platform=os.path.join(pfm_dir, 'kv260', 'export', 'kv260', 'kv260.xpfm'),
    template='installed_examples/vadd'
)

proj.build(target='hw')

vitis.dispose()
